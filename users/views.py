import logging
from base64 import b64encode
from datetime import datetime
from threading import Thread
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy.orm.exc import NoResultFound

from app import login_manager
from utils.access_rights import check_confirmed
from utils.api import create_jwt
from organization.models import Organization
from users.forms import RegisterForm, SignInForm, EditForm, ForgotPasswordForm, RestorePasswordForm, NotificationForm
from users.models import User, Course
from users.utils import token_to_email, send_confirm_message, create_or_update_user
from flask.views import MethodView
from utils.email import send_email


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_required
@check_confirmed
def profile():
    return render_template('users/profile.html')


@login_required
def logout():
    logout_user()
    return redirect(url_for("news.index"))


@login_required
@check_confirmed
def personnel():
    org: Organization = current_user.binded_org
    if org is None:
        abort(404)
    organization_info = {
        'org': org,
        'workers': org.exists_workers,
        'required_workers': org.required_workers,
    }

    return render_template('users/personnel.html', **organization_info, len=len)


def education():
    return render_template("users/education.html",
                           courses=Course.query.order_by(Course.start.desc()), b64encode=b64encode)


@login_required
@check_confirmed
def notification():
    form = NotificationForm()
    if form.validate_on_submit():
        pass  # TODO: Сделать уведомления
    return render_template('users/notifications.html', form=form)


@login_required
@check_confirmed
def t2(user_id):
    target = User.get(user_id)
    if not target.has_user_permission(current_user):
        abort(403)

    if target is None or not target.t2_rel:
        abort(404)

    return render_template("users/T2.html", form=target.t2_rel)


class EditProfile(MethodView):
    decorators = [check_confirmed, login_required]

    def get(self):
        form = EditForm(obj=current_user)
        return render_template('users/edit_profile.html',
                               form=form, orgs=current_user.organizations)

    def post(self):
        form = EditForm()
        if not create_or_update_user(form)["ok"]:
            return self.get()

        logging.info(f"{current_user} updated profile")

        return redirect(url_for('users.profile'))


class Login(MethodView):
    def get(self):
        form = SignInForm()
        return render_template('users/sign_in.html', form=form)

    def post(self):
        form = SignInForm()
        if form.validate_on_submit():
            user = User.get_logged(form.email.data, form.password.data)
            if user is not None:
                login_user(user)
                return redirect(url_for('users.profile'))
        return self.get()


class Registration(MethodView):
    def get(self):
        form = RegisterForm()
        return render_template("users/registration.html", form=form)

    def post(self):
        form = RegisterForm()
        res = create_or_update_user(form)
        if not res["ok"]:
            return self.get()

        user = res["user"]

        logging.info(f"Зарегистрирован пользователь: {user}")
        login_user(user)
        return redirect(url_for('users.profile'))


def confirm_email():
    token = request.args['token']
    email = token_to_email(token)

    user = User.query.filter_by(email=email).first_or_404()
    if not current_user.is_authenticated:
        login_user(user)

    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
        return redirect(url_for('news.index'))

    user.confirmed = True
    user.save()
    logging.info(f"Account confirmed {user} {user.confirmed}")
    flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('news.index'))


class RestorePassword(MethodView):
    def get(self):
        form = RestorePasswordForm()
        return render_template('users/forgot_password.html', form=form)

    def post(self):
        form = RestorePasswordForm()
        if not form.validate_on_submit():
            return self.get()
        user = User.get_by(email=form.email.data)
        if not user:
            abort(404)
        user.restore_token = create_jwt(datetime.now().timestamp())
        user.save()

        confirm_url = url_for('change_password', email=form.email.data, token=user.restore_token, _external=True)
        html = render_template('activate_mess.html', confirm_url=confirm_url)

        Thread(target=send_email, args=(user.email, html, "Restore your GosRab password")).run()

        return 'Ok'


class ChangePassword(MethodView):
    def get(self):
        form = ForgotPasswordForm()
        return render_template('users/forgot_password.html', form=form)

    def post(self, email, token):
        form = ForgotPasswordForm()
        if not form.validate_on_submit():
            return self.get()

        user = User.get_by(email=email)
        if user.restore_token != token:
            abort(403)

        user.set_password(form.password.data)
        user.restore_token = None
        user.save()
        login_user(user)
        return redirect(url_for('users.profile'))
