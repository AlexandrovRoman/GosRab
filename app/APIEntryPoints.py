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
        if not user:
            return jsonify({'error': 'incorrect email or password'})
        session['current_user_jwt'] = create_jwt(user.to_dict(only=('id', 'name', 'surname', 'fathername', 'email')))
        return jsonify({'authorization': 'OK'})

    def delete(self):
        session.pop('current_user_jwt', None)
        return jsonify({'sign out': 'OK'})

    @staticmethod
    def get_authorized_user():
        try:
            return User.get(jwt.decode(session['current_user_jwt'], Config.JWT_SECRET_KEY)['payload']['id'])
        except (TypeError, KeyError):
            return None


class OrgApiEntryPoint(Resource):
    def get(self, org_id, jwt):
        org = Organization.get_by(id=org_id)
        if org and check_tokens(jwt, org.api_token):
            session['current_org_jwt'] = create_jwt(org.to_dict(only=('id', 'name')))
            return jsonify({'authorization': 'OK'})
        return jsonify({'error': 'incorrect Organization ID or JWT'})

    def delete(self):
        session.pop('current_org_jwt', None)
        return jsonify({'sign out of organization': 'OK'})

    @staticmethod
    def get_authorized_org():
        try:
            return Organization.get_by(
                id=jwt.decode(session['current_org_jwt'], Config.JWT_SECRET_KEY)['payload']['id'])
        except (TypeError, KeyError):
            return None
