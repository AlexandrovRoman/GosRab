from app.tokens import create_jwt
from flask_restful import Resource
from users.models import User
import jwt
from app.config import Config
from flask import session, jsonify


class UserLoginResource(Resource):

    def get(self, email, password):
        user = User.get_logged(email, password)
        if user:
            session['current_user_jwt'] = create_jwt(
                user.to_dict(only=('id', 'name', 'surname', 'fathername', 'email')))
            return jsonify({'authorization': 'OK'})
        return jsonify({'error': 'incorrect email or password'})

    @classmethod
    def return_authorized_user(self):
        if 'current_user_jwt' in session:
            return User.get(jwt.decode(session['current_user_jwt'], Config.JWT_SECRET_KEY)['payload']['id'])
        return None


class BasicResource(Resource):

    def basic_error(self, message):
        return jsonify({'error': message})

    def set_authorized_user(self):
        self.authorized_user = UserLoginResource.return_authorized_user()
