from flask import render_template, request, make_response, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app import login_manager, session
from users.models import User


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@login_required
def profile():
    user = current_user
    return render_template('users/profile.html', **user.get_profile_info)


@login_required
def edit_profile():
    user = current_user
    if request.method == 'POST':
        # print('\n\t', current_user, '\n')

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
    return render_template('users/edit_profile.html', **user.get_profile_info)


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


def login():
    if request.method == 'POST':
        user = User.get_logged(request.form['username'], request.form['password'])
        if user is not None:
            login_user(user)
            return redirect('/')

    return render_template('users/sign_in.html')


def logout():
    logout_user()
    return redirect('/')


def personnel():
    organizations = current_user.get_organizations()
    workers = sum((i[1] for i in organizations))
    vacancy = sum((i[2] for i in organizations))

    return render_template('users/personnel.html', organizations=organizations,
                           stats=(workers, vacancy))


def education():
    return render_template("users/education.html", courses=[
        ('Курсы', 'Яндекс Лицей', 'Сентябрь 2018', 'Обучение програмированию на языке Python на базе компании Яндекс.',
         'icon/yandex.jpg'),
        ('Онлайн обучение', 'Super-English', 'Февраль 2020',
         'Изучение английского языка с нуля, до свободного общения вместе с Петровой Оксаной Сергеевной.',
         'icon/English.jpg'),
    ])


def notification():
    return render_template("users/notifications.html")


def personnel_department():
    return render_template("personnel_department.html")
