from datetime import datetime
from threading import Thread
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import login_manager
from users.forms import RegisterForm, SignInForm, EditForm
from users.models import User, Course
from users.utils import check_confirmed, generate_confirmation_token, send_email, confirm_token


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_required
@check_confirmed
def profile():
    return render_template('users/profile.html')


@login_required
@check_confirmed
def edit_profile():
    form = EditForm()
    user = current_user
    if not form.validate_on_submit():
        for i in ['surname', 'name',
                  'fathername', 'sex',
                  'marriage', 'email',
                  'birth_date', 'about_myself',
                  ]:
            form[i].data = getattr(user, i)
        return render_template('users/edit_profile.html', user=user, form=form)

    ignore = ("birth_date",)
    setattr(user, "birth_date", datetime.strptime(request.form["birth_date"], "%Y-%m-%d").date())
    for attr in request.form:
        if attr not in ignore:
            setattr(user, attr, request.form[attr])

    user.save()

    return redirect(url_for('profile'))


def login():
    form = SignInForm()
    if form.validate_on_submit():
        user = User.get_logged(request.form['email'], request.form['password'])
        if user is not None:
            login_user(user)
            return redirect('/')

    return render_template('users/sign_in.html', form=form)


@login_required
def logout():
    logout_user()
    return redirect('/')


@login_required
@check_confirmed
def personnel():
    org = current_user.binded_org
    if org is None:
        return 'Не привязан ни к одной'
    organization_info = {
        'org': org,
        'workers': org.get_workers(),
        'required_workers': org.get_required_workers(),
    }

    return render_template('users/personnel.html', **organization_info, len=len)


def education():
    return render_template("users/education.html", courses=Course.get_courses())


@login_required
@check_confirmed
def notification():
    return render_template('users/notifications.html')


def registration():
    form = RegisterForm()
    if not form.validate_on_submit():
        return render_template("users/registration.html", form=form)
    if User.get_by(email=request.form['email']):
        return 'Email уже использован'
    birth_date = datetime.strptime(request.form["birth_date"], "%Y-%m-%d").date()

    user = User(request.form['name'], request.form['surname'],
                request.form['fathername'], request.form['email'],
                request.form['password'], sex=request.form['sex'], birth_date=birth_date)

    token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    html = render_template('activate_mess.html', confirm_url=confirm_url)

    Thread(target=send_email, args=(user.email, html, "Confirm your GosRab account")).run()

    user.save(add=True)

    print('Зарегистрирован пользователь:', user)
    login_user(user)
    return redirect('/users/profile')


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
    return redirect('/')


@login_required
@check_confirmed
def t2():
    user_id = request.args['user_id']
    user = current_user
    if False:  # TODO: Если не обладает правами кадровика над человеком с user_id
        return 'Нет доступа к форме этого пользователя'
    target = User.get(user_id)

    # TODO: Create html templates
    if target is None:
        return 'Нет пользователя'
    if not target.t2_rel:  # Если не обладает формой T2
        return 'Нет формы T2'

    return render_template("users/T2.html", form=target.t2_rel[0])
