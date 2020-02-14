from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    surname = db.Column(db.String(80), nullable=True)
    fathername = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(40),
                      index=True, unique=True, nullable=True)
    # hashed_password = db.Column(db.String, nullable=True)
    # birth_date = db.Column(db.Date, nullable=
    age = db.Column(db.Integer)
    sex = db.Column(db.String(1), nullable=True) # М/Ж
    status = db.Column(db.String, nullable=True,
                       default='standart_user')  # standart_user, admin, organistaion, superuser
    grate = db.Column(db.String, default='Новичок')
    education = db.Column(db.String, default='Нет')
    foreign_languges = db.Column(db.String, default='Нет')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
