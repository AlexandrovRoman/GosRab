from functools import wraps
from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer

from app import app
# from flask.ext.mail import Message


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.confirmed is False:
            return 'Please confirm your account!'
        return func(*args, **kwargs)

    return decorated_function


# def send_email(to, subject, template):
#     msg = Message(
#         subject,
#         recipients=[to],
#         html=template,
#         sender=app.config['MAIL_DEFAULT_SENDER']
#     )
#     mail.send(msg)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email
