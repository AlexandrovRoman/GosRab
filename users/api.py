from flask import jsonify
from flask_login import current_user
from flask_restful import reqparse, Resource
from app.api import abort_obj_not_found
from users.models import User


def abort_user_not_found(user_id):
    abort_obj_not_found(user_id, User)


class UserResource(Resource):
    def get(self, user_id):
        abort_user_not_found(user_id)
        user = User.get(user_id)
        if user.id != getattr(current_user, "id", None):
            return jsonify({'user': 'Operation not allowed to this user'})
        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'surname', 'fathername', 'birth_date'))})

    def delete(self, user_id):
        abort_user_not_found(user_id)
        if user_id != getattr(current_user, "id", None):
            return jsonify({'deleting': 'Operation not allowed to this user'})
        user = User.get(user_id)
        user.delete()
        return jsonify({'deleting': 'OK'})


class UserListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('surname', required=True)
    parser.add_argument('fathername', required=True)
    parser.add_argument('email', required=True)
    parser.add_argument('password', required=True)

    def get(self):
        # Кто может смотреть данные всех юзеров?
        users = User.all()
        return jsonify({'user': [user.to_dict(
            only=('id', 'name', 'surname', 'fathername', 'birth_date')) for user in users]})

    def post(self):
        # Кто может добавить юзера?
        args = self.parser.parse_args()
        user = User(
            name=args['name'],
            surname=args['surname'],
            fathername=args['fathername'],
            email=args['email'],
        )
        user.set_password(args['password'])
        user.save(add=True)
        return jsonify({'adding': 'OK'})
