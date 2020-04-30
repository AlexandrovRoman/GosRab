import jwt
import datetime
from app.config import BaseConfig


def create_jwt(subject, exp_days=7):
    token = jwt.encode({
        'sub': subject,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=exp_days)},
        BaseConfig.JWT_SECRET_KEY, algorithm='HS256')
    return token


def check_tokens(token_a, token_b):
    return jwt.decode(token_a, BaseConfig.JWT_SECRET_KEY)['sub'] == jwt.decode(token_b, BaseConfig.JWT_SECRET_KEY)[
        'sub']
