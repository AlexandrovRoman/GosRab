import re
import jwt
from flask import jsonify, session
from flask_restful import reqparse, Resource
from app import Config
from users.models import User
from utils.api import get_or_abort, BasicResource as _BasicResource, jwt_login_required, create_jwt
from .views import Registration


def get_or_abort_user(user_id):
    return get_or_abort(user_id, User)


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


class BasicUserResource(_BasicResource):
    def set_authorized_user(self):
        self.authorized_user = UserApiEntryPoint.get_authorized_user()


class UserResource(BasicUserResource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('surname', required=True)
    parser.add_argument('fathername', required=True)
    parser.add_argument('email', required=True)
    parser.add_argument('password', required=True)

    @jwt_login_required
    def get(self, user_id):
        user = get_or_abort_user(user_id)
        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'surname', 'fathername', 'birth_date'))})

    @jwt_login_required
    def delete(self, user_id):
        user = get_or_abort_user(user_id)
        if user_id != self.authorized_user.id:
            return self.basic_error('delete is not allowed to this user')

        user.delete()
        return jsonify({'deleting': 'OK'})

    def post(self):
        args = self.parser.parse_args()
        if User.get_by(email=args['email']):
            return self.basic_error('email already taken')

        if any(map(str.isdigit, args['name'] + args['surname'] + args['fathername'])):
            return self.basic_error('invalid name, surname or fathername')

        if not re.search(r".+@.+\..+", args["email"]):
            return self.basic_error('invalid email')

        user = User(
            name=args['name'],
            surname=args['surname'],
            fathername=args['fathername'],
            email=args['email'],
            password=args['password']
        )
        user.save(add=True)
        Registration.send_email(user)
        return jsonify({'adding': 'OK', 'user': user.to_dict(
            only=('id', 'name', 'surname', 'fathername', 'birth_date'))})
