from app.tokens import create_jwt, check_tokens
from flask_restful import Resource
from users.models import User
from organization.models import Organization
import jwt
from app.config import Config
from flask import session, jsonify


class UserApiEntryPoint(Resource):
    def get(self, email, password):
        user = User.get_logged(email, password)
        if user:
            session['current_user_jwt'] = create_jwt(
                user.to_dict(only=('id', 'name', 'surname', 'fathername', 'email')))
            return jsonify({'authorization': 'OK'})
        return jsonify({'error': 'incorrect email or password'})

    def delete(self):
        if 'current_user_jwt' in session:
            del session['current_user_jwt']
        return jsonify({'sign out': 'OK'})

    @staticmethod
    def get_authorized_user():
        if 'current_user_jwt' in session:
            return User.get(jwt.decode(session['current_user_jwt'], Config.JWT_SECRET_KEY)['payload']['id'])
        return None


class OrgApiEntryPoint(Resource):
    def get(self, org_id, jwt):
        org = Organization.get_by(id=org_id)
        if org and check_tokens(jwt, org.api_token):
            session['current_org_jwt'] = create_jwt(
                org.to_dict(only=('id', 'name')))
            return jsonify({'authorization': 'OK'})
        return jsonify({'error': 'incorrect Organization ID or JWT'})

    def delete(self):
        if 'current_org_jwt' in session:
            del session['current_org_jwt']
        return jsonify({'sign out of organization': 'OK'})

    @staticmethod
    def get_authorized_org():
        if 'current_org_jwt' in session:
            return Organization.get_by(
                id=jwt.decode(session['current_org_jwt'], Config.JWT_SECRET_KEY)['payload']['id'])
        return None


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
