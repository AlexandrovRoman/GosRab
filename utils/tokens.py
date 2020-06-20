import jwt
import datetime
from app.config import Config


def create_jwt(payload, exp_days=7):
    token = jwt.encode({
        'payload': payload,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=exp_days)},
        Config.JWT_SECRET_KEY, algorithm='HS256')
    return token.decode("utf-8")


def check_tokens(token_a, token_b):
    try:
        return jwt.decode(token_a, Config.JWT_SECRET_KEY)['payload'] == jwt.decode(token_b,
                                                                                   Config.JWT_SECRET_KEY)['payload']
    except jwt.exceptions.DecodeError:
        return False
