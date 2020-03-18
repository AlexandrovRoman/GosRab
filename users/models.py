import datetime
from flask_login import UserMixin
from app import db, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import base_new

roles_relationship = db.Table('roles_relationship',
                              db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                              db.Column('role_id', db.Integer, db.ForeignKey('roles.role_id')))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    name = db.Column(db.String(80), nullable=True)
    surname = db.Column(db.String(80), nullable=True)
    fathername = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(40),
                      index=True, unique=True, nullable=True)
    hashed_password = db.Column(db.String, nullable=True)
    birth_date = db.Column(db.Date)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(7), nullable=True)  # М/Ж
    grate = db.Column(db.String, default='Новичок')
    education = db.Column(db.String, default='Отсутствует')
    foreign_languges = db.Column(db.String, default='Отсутствует')
    start_place = db.Column(db.String)
    nationality = db.Column(db.String)
    marriage = db.Column(db.String(20))
    about_myself = db.Column(db.String, default='Отсутствует')
    # organization info
    salary = db.Column(db.Integer, nullable=True)
    post = db.Column(db.String, nullable=True)
    work_place_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True)
    work_department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=True)
    roles = db.relationship('Role', secondary=roles_relationship, backref=db.backref('users', lazy='dynamic'))

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @property
    def get_profile_info(self):
        return {'Surname': self.surname, 'Name': self.name, 'Middle_name': self.fathername,
                'Gender': self.sex, 'Age': self.age, 'Grade': self.grate,
                'Education': self.education, 'Marital_status': self.marriage,
                'Knowledge_of_foreign_language': self.foreign_languges, 'Email': self.email,
                'About_myself': self.about_myself, 'Workplace': 'Автосервис Михаил-авто(отдел продаж) - Глав.Менеджер'}

    @classmethod
    def get_logged(cls, login, password):
        user = session.query(cls).filter(cls.email == login).first()
        if user and user.check_password(password):
            return user
        return None

    @classmethod
    def get(cls, user_id):
        return session.query(cls).filter(cls.id == user_id).first()

    @classmethod
    def new(cls, surname, name, fathername, birth_year, birth_month, birth_day,
            age, email, password, sex, marriage, org_id, roles='user'):
        kwargs = {"surname": surname, "name": name, "fathername": fathername,
                  "birth_date": datetime.date(birth_year, birth_month, birth_day),
                  "age": age, "email": email, "hashed_password": generate_password_hash(password),
                  "sex": sex, "marriage": marriage, "organization_foreign_id": org_id}
        special_commands = (f"cls.add_roles(obj, '{roles}')",)
        base_new(cls, special_commands, **kwargs)

    @staticmethod
    def add_roles(user, role_names):
        for role_name in role_names.split():
            role = Role.get_role_for_name(role_name)
            local_session_role = session.merge(role)
            user.roles.append(local_session_role)
        session.commit()


class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer,
                        primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(200))

    @classmethod
    def new(cls, name, description):
        kwargs = {"role_name": name, "description": description}
        base_new(cls, **kwargs)

    def __repr__(self):
        return '<Role {}, Возможности:{}>'.format(self.role_name, self.description)

    @classmethod
    def get_role_for_name(cls, role_name):
        return cls.query.filter_by(role_name=role_name).first()


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_type = db.Column(db.String(20))
    course_name = db.Column(db.String(70))
    data = db.Column(db.String(20))  # TODO: сделать в формате начало - конец
    description = db.Column(db.String)
    image = db.Column(db.String(20))  # TODO: хранить картинку в юазе данных

    @classmethod
    def new(cls, course_type, name, data, description, image):
        kwargs = {"course_type": course_type, "course_name": name,
                  "data": data, "description": description, "image": image}
        base_new(cls, **kwargs)

    @classmethod
    def get_courses(cls):
        courses = [(obj.course_type, obj.course_name, obj.data, obj.description, obj.image) for obj in cls.query.all()]
        return courses


# ЭТО ЗАГЛУШКА НЕ УДАЛЯТЬ
class Model1(db.Model):
    __tablename__ = 'model1'
    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
