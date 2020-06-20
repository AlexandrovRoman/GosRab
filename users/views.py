from base64 import b64encode
from datetime import datetime
from threading import Thread
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from app import login_manager
from utils.tokens import create_jwt
from organization.models import Organization
from users.forms import RegisterForm, SignInForm, EditForm, ForgotPasswordForm, RestorePasswordForm, NotificationForm
from users.models import User, Course
from users.utils import check_confirmed, generate_confirmation_token, send_email, confirm_token
from flask.views import MethodView


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
    org = current_user.binded_org
    if org is None:
        return abort(404)
    organization_info = {
        'org': org,
        'workers': org.get_workers(),
        'required_workers': org.get_required_workers(),
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
        return abort(403)

    if target is None:
        return abort(404)
    if not target.t2_rel:  # Если не обладает формой T2
        return abort(404)

    return render_template("users/T2.html", form=target.t2_rel[0])


class EditProfile(MethodView):
    decorators = [check_confirmed, login_required]

    def get(self):
        form = EditForm()
        for field in ['surname', 'name',
                      'fathername', 'sex',
                      'marriage', 'email',
                      'birth_date', 'about_myself',
                      ]:
            form[field].data = getattr(current_user, field)
        return render_template('users/edit_profile.html', form=form, orgs=Organization.get_attached_to_user(current_user))

    def post(self):
        form = EditForm()
        if not form.validate_on_submit():
            return self.get()
        ignore = ("birth_date",)
        setattr(current_user, "birth_date", datetime.strptime(request.form["birth_date"], "%Y-%m-%d").date())
        for attr in request.form:
            if attr not in ignore:
                setattr(current_user, attr, request.form[attr])
        current_user.save()
        return redirect(url_for('users.profile'))


class Login(MethodView):
    def get(self):
        form = SignInForm()
        return render_template('users/sign_in.html', form=form)

    def post(self):
        form = SignInForm()
        if form.validate_on_submit():
            user = User.get_logged(request.form['email'], request.form['password'])
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
        if not form.validate_on_submit():
            return self.get()
        if User.get_by(email=request.form['email']):
            return 'Email уже использован'
        birth_date = datetime.strptime(request.form["birth_date"], "%Y-%m-%d").date()
        user = User(request.form['name'], request.form['surname'],
                    request.form['fathername'], request.form['email'],
                    request.form['password'], sex=request.form['sex'], birth_date=birth_date)
        self.send_email(user)
        user.save(add=True)
        print('Зарегистрирован пользователь:', user)
        login_user(user)
        return redirect(url_for('users.profile'))

    @staticmethod
    def send_email(user):
        token = generate_confirmation_token(user.email)
        confirm_url = url_for('users.confirm_email', token=token, _external=True)
        html = render_template('activate_mess.html', confirm_url=confirm_url)

        Thread(target=send_email, args=(user.email, html, "Confirm your GosRab account")).run()


def confirm_email():
    token = request.args['token']
    email = confirm_token(token)
    user = User.query.filter_by(email=email).first_or_404()
    if not current_user.is_authenticated:
        login_user(user)
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        user.save()
        print('Account confirmed', user, user.confirmed)
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
            return abort(404)
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
            return abort(403)
        user.set_password(form.password.data)
        user.restore_token = None
        user.save()
        login_user(user)
        return redirect(url_for('users.profile'))
