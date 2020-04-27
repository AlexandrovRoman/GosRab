from flask_restful import reqparse, abort, Resource
from flask import jsonify
from app import db
from app import session
from users.models import User
from organization.models import Organization
from flask_login import current_user


def abort_user_not_found(user_id):  # По идее можно обобщить для всех классов
    obj = User.get(user_id)
    if not obj:
        abort(404, message=f"User with id {user_id} not found")


class UserResource(Resource):
    def get(self, user_id):
        abort_user_not_found(user_id)
        user = User.get(user_id)
        if user.id != current_user.id:
            return jsonify({'user': 'Operation not allowed to this user'})
        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'surname', 'fathername', 'birth_date'))})

    def delete(self, user_id):
        abort_user_not_found(user_id)
        if user_id != current_user.id:
            return jsonify({'deleting': 'Operation not allowed to this user'})
        user = User.get(user_id)
        session.delete(user)
        session.commit()  # Нужно ли тут заменить session?
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
        users = session.query(User).all()  # Можно ли тут заменить session на методы ModelMixin?
        return jsonify({'user': [user.to_dict(
            only=('id', 'name', 'surname', 'fathername', 'birth_date')) for user in users]})

    def post(self):
        # Кто может добавить юзера?
        args = parser.parse_args()
        user = User(
            name=args['name'],
            surname=args['surname'],
            fathername=args['fathername'],
            email=args['email'],
        )
        user.set_password(args['password'])
        user.save(add=True)
        return jsonify({'adding': 'OK'})
