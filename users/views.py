from flask import render_template, request, make_response, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import create_session, login_manager
from users.models import User
import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_required
def profile():
    user = current_user
    return render_template('profile.html',
                           Surname=user.surname, Name=user.name, Middle_name=user.fathername, Gender=user.sex,
                           Age=user.age, Grade=user.grate, Education=user.education, Marital_status=user.marriage,
                           Knowledge_of_foreign_language=user.foreign_languges)


@login_required
def edit_profile():
    user = current_user
    if request.method == 'POST':
        # print('\n\t', current_user, '\n')
        session = create_session()

        current_user.name = request.form['name']
        current_user.surname = request.form['surname']
        current_user.fathername = request.form['middlename']
        current_user.age = request.form['age']
        current_user.email = request.form['email']
        current_user.sex = request.form['gender']
        current_user.marriage = request.form['maritalstatus']
        # current_user.about = request.form['aboutmyself'] Отсутствует столбец

        session.merge(current_user)
        session.commit()

        return redirect(url_for('profile'))
    return render_template('edit_profile.html', Surname=user.surname, Name=user.name, Middle_name=user.fathername,
                           Gender=user.sex,
                           Age=user.age, Grade=user.grate, Education=user.education, Marital_status=user.marriage,
                           Knowledge_of_foreign_language=user.foreign_languges, Email=user.email)


@login_required
def cookie_test():
    print(current_user)
    print(type(current_user))
    print(isinstance(current_user, User))
    print(current_user.name)
    print(current_user.surname)
    print(current_user.fathername)
    print(current_user.email)
    cook = request.cookies.get('click')
    click_count = cook if cook else '2'
    res = make_response(f"Your click count is {click_count}")
    res.set_cookie('click', str(int(click_count) + 1), max_age=1)

    return res


def user_add(surname, name, fathername, birth_year, birth_month, birth_day, age, email, password, sex, role='user'):
    session = create_session()
    user = User()
    user.surname = surname
    user.name = name
    user.age = age
    user.fathername = fathername
    user.hashed_password = user.set_password(password)
    user.birth_date = datetime.date(birth_year, birth_month, birth_day)
    user.sex = sex
    user.email = email
    user.role = role
    user.set_password(password)
    session.add(user)
    session.commit()


def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    # form = LoginForm()
    if request.method == 'POST':
        user = User.get_logged(request.form['username'], request.form['password'])
        if user is not None:
            login_user(user)
            return redirect('/')

    # if form.validate_on_submit():
    # Login and validate the user.
    # user should be an instance of your `User` class
    # login_user()
    #
    # flask.flash('Logged in successfully.')
    #
    # next = flask.request.args.get('next')
    # is_safe_url should check if the url is safe for redirects.
    # See http://flask.pocoo.org/snippets/62/ for an example.
    # if not is_safe_url(next):
    #     return flask.abort(400)

    # return flask.redirect(next or flask.url_for('index'))
    return render_template('sign_in.html')  # , form=form)


def logout():
    logout_user()
    return redirect('/')


def personnel():
    return render_template('personnel.html')


def education():
    return render_template("education.html")
