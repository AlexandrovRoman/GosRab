from flask import jsonify
from flask_restful import abort, Resource

from app.APIEntryPoints import UserApiEntryPoint, OrgApiEntryPoint


def get_or_abort(id_, cls):
    obj = cls.get_by(id=id_)
    if not obj:
        abort(404, message=f"{cls.__name__} with id {id_} not found")
    return obj


class BasicResource(Resource):
    @staticmethod
    def basic_error(message):
        return jsonify({'error': message})

    def set_authorized_user(self):
        self.authorized_user = UserApiEntryPoint.get_authorized_user()

    def set_authorized_org(self):
        self.authorized_org = OrgApiEntryPoint.get_authorized_org()


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

