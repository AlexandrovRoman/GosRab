import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase, create_session
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    fathername = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String,
                              index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    # birth_date = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.String, nullable=True,
                               default='standart_user')  # standart_user, admin, organistaion, superuser

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)


session = create_session()
for i in range(1, 5):
    user = User()
    user.name = f"Имя {i}"
    user.surname = f'Фамилия {i}'
    user.fathername = f'Отчество {i}'
    user.email = f"email{i}@email.ru"
    user.set_password(f'password_{i}')
    # user.birth_date = datetime.date(1998, 7, i)
    session.add(user)
    session.commit()
