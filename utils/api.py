from flask import jsonify
from flask_restful import abort, Resource
import jwt
import datetime
from app.config import Config


def get_or_abort(id_, cls):
    obj = cls.get_by(id=id_)
    if not obj:
        abort(404, message=f"{cls.__name__} with id {id_} not found")
    return obj


class BasicResource(Resource):
    @staticmethod
    def basic_error(message):
        return jsonify({'error': message})


def jwt_login_required(method):
    def check_API_rights(self, **kwargs):
        self.set_authorized_user()
        if not self.authorized_user:
            return self.basic_error('Login before using API')
        return method(self, **kwargs)

    return check_API_rights


def jwt_org_required(method):
    def check_API_rights(self, **kwargs):
        self.set_authorized_org()
        if not self.authorized_org:
            return self.basic_error('Login with your organization before using Organizations API')
        return method(self, **kwargs)

    return check_API_rights


def create_jwt(payload, exp_days=7):
    token = jwt.encode({
        'payload': payload,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=exp_days)},
        Config.JWT_SECRET_KEY, algorithm='HS256')
    return token.decode("utf-8")


def check_tokens(token_a, token_b):
    try:
        return (jwt.decode(token_a, Config.JWT_SECRET_KEY)['payload']
                == jwt.decode(token_b, Config.JWT_SECRET_KEY)['payload'])
    except jwt.exceptions.DecodeError:
        return False
