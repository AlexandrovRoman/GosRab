import logging
from threading import Thread
from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask import current_app, url_for, render_template
from users.models import User
from utils.email import send_email
from typing import Union, Optional, Dict
from users.forms import RegisterForm, EditForm


def token_to_email(token, expiration=3600) -> Optional[str]:
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        return serializer.loads(
            token,
            salt=current_app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except (SignatureExpired, BadSignature) as ex:
        logging.warning(f"{ex.__class__.__name__}: {ex}")
        return None


def _generate_confirmation_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])


def send_confirm_message(email: str) -> None:
    token = _generate_confirmation_token(email)
    confirm_url = url_for('users.confirm_email', token=token, _external=True)
    html = render_template('activate_mess.html', confirm_url=confirm_url)

    Thread(target=send_email, args=(email, html, "Confirm your GosRab account")).run()

    logging.info(f"Confirmation message has been sent to {email}")


def create_or_update_user(form: Union[RegisterForm, EditForm]) -> Dict[str, Union[bool, str]]:
    if not form.validate_on_submit():
        return {"ok": False, "error": "Invalid form"}

    user: User = current_user if isinstance(current_user, User) else User()

    if user.email != form.email.data:
        if User.query.filter_by(email=form.email.data).count() > 0:
            return {"ok": False, "error": "Email used"}
        send_confirm_message(form.email.data)
        user.confirmed = False

    form.populate_obj(user)
    user.save()

    return {"ok": True, "user": user}
