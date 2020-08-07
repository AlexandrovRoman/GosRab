from functools import wraps
from flask import render_template
from flask_login import current_user


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            return render_template('users/not_confirmed.html',
                                   error='Не подтверждена почта',
                                   discription='Вам было прислано письмо, пожалуйста перейдите '
                                               'по ссылке и подтвердите вашу почту')
        return func(*args, **kwargs)

    return decorated_function
