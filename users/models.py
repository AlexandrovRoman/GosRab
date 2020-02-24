from flask_login import UserMixin
from app import create_session
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm

role_list = ['standart_user', 'admin', 'organistaion', 'superuser']


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    surname = db.Column(db.String(80), nullable=True)
    fathername = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(40),
                      index=True, unique=True, nullable=True)
    hashed_password = db.Column(db.String, nullable=True)
    birth_date = db.Column(db.Date)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(20), nullable=True)  # М/Ж
    status = db.Column(db.String, nullable=True,
                       default=role_list[0])
    grate = db.Column(db.String, default='Новичок')
    education = db.Column(db.String, default='Нет')
    foreign_languges = db.Column(db.String, default='Нет')
    role = db.Column(db.String, default='user')
    start_place = db.Column(db.String)
    nationality = db.Column(db.String)
    marriage = db.Column(db.String(10))
    about_myself = db.Column(db.String)
    # organisation = orm.relation('Organisation', back_populates='organisation')
    # about_myself = db.Column(db.String)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @staticmethod
    def get_logged(login, password):
        session = create_session()
        user = session.query(User).filter(User.email == login).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def get(user_id):
        session = create_session()
        return session.query(User).filter(User.id == user_id).first()

# ЭТО ЗАГЛУШКА НЕ УДАЛЯТЬ
class Model1(db.Model):
    __tablename__ = 'model1'
    id = db.Column(db.Integer,
                    primary_key=True, autoincrement=True)