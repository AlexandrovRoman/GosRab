from flask import jsonify
from flask_login import current_user
from flask_restful import reqparse, Resource
from app.api_utils import abort_obj_not_found
from users.models import User
from .views import Registration


def abort_user_not_found(user_id):
    abort_obj_not_found(user_id, User)


class UserResource(Resource):
    def get(self, user_id):

        # Тут по сути дублируется запрос к бд, посмотри как оптимизировать
        abort_user_not_found(user_id)
        user = User.get(user_id)

        # Наверное слишком, достаточно чтобы пользователь просто был авторизован
        if user.id != getattr(current_user, "id", None):
            return jsonify({'user': 'Operation not allowed to this user'})

        return jsonify({'user': user.to_dict(
            only=('id', 'name', 'surname', 'fathername', 'birth_date'))})

    def delete(self, user_id):
        abort_user_not_found(user_id)
        # Нужно придумать как авторизовываться, через url нужно делать первый запрос со своими данными,
        # сервер должен записать тебя в сессию. И тогда уже возможны данные проверки
        # Короче нужно что-то типо init запроса, в котором будет создаваться сессия с конкретным токеном
        # (или данными пользователя)
        if user_id != getattr(current_user, "id", None):
            return jsonify({'deleting': 'Operation not allowed to this user'})
        user = User.get(user_id)
        user.delete()
        return jsonify({'deleting': 'OK'})


class UserListResource(Resource):
    """Что тут делает создание пользователя?!
    Тут ведь вроде должны лежать действия с группой пользователей. Короче наверное стоит удалить"""

    parser = reqparse.RequestParser()
    parser.add_argument('name', required=True)
    parser.add_argument('surname', required=True)
    parser.add_argument('fathername', required=True)
    parser.add_argument('email', required=True)
    parser.add_argument('password', required=True)

    def post(self):
        # Почему нет никакой валидации аргументов?
        args = self.parser.parse_args()
        if User.get_by(email=args['email']):
            return jsonify({'error': 'email already taken'})
        user = User(
            name=args['name'],
            surname=args['surname'],
            fathername=args['fathername'],
            email=args['email'],
            password=args['password']
        )
        user.save(add=True)

        # Если создавать пользователя буз этого, то аккаунт будет бесполезным, т.к его нельзя будет подтвердить
        Registration.send_email(user)

        return jsonify({'adding': 'OK'})
