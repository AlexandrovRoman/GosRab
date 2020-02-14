from typing import List, Tuple
from flask import render_template, request, make_response
from app import create_session
from users.models import User
import datetime

current_users: List[Tuple[str, str]] = [
    ('aaa', '111'),
    ('ggg', '123'),  # эта чоита?
]


def profile():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for i, j in current_users:
            if i == username and j == password:
                return render_template('news.html')

        # return render_template('news.html')
    return render_template('profile.html')


def cookie_test():
    cook = request.cookies.get('click')
    click_count = cook if cook else '2'
    res = make_response(f"Your click count is {click_count}")
    res.set_cookie('click', str(int(click_count) + 1), max_age=1)

    return res


def index():
    return render_template('news.html')

def user_add(surname,name, fathername, birth_year, birth_month, birth_day, email, password, sex):
    session = create_session()
    user = User()
    user.surname = surname
    user.name = name
    user.fathername = fathername
    # user.birth_date = datetime.date(birth_year, birth_month, birth_day)
    user.sex = sex
    user.email = email
    # user.set_password(password)
    session.add(user)
    session.commit()


