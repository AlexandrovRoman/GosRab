import datetime
from flask_login import UserMixin
from app import create_session
from app import db, session
from werkzeug.security import generate_password_hash, check_password_hash

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

    @property
    def get_profile_info(self):
        return {'Surname': self.surname, 'Name': self.name, 'Middle_name': self.fathername,
                'Gender': self.sex, 'Age': self.age, 'Grade': self.grate,
                'Education': self.education, 'Marital_status': self.marriage,
                'Knowledge_of_foreign_language': self.foreign_languges, 'Email': self.email}

    def get_organizations(self):  # todo Наименование, Рабочие, Вакансии, id организации
        return [('Хлебобулочный комбинат', 0, 0, 1),
                ('ПФР пром. района', 1000, 500, 2),
                ('Автосервис Михаил-авто', 666, 69, 3)]

    def get_organization(self, org_id):
        if org_id is None:
            return None
        if org_id not in ['1', '2', '3']:  # Если пользователь не состоит в этой организации
            return None
        # Вернуть в зависимость от org_id
        return {'required_employees': enumerate([('Кондитер', 30000), ('Директор', 50000)], 1),
                'workers': [('Карпов Павел Андреевич', 'Кондитер', 30000),
                           ('Денисов Шамиль Вадимович', 'Директор', 50000),
                           ('Федункив Сава Богданович', 'Администратор', 25000),
                           ('Бирюков Мирослав Васильевич', 'Кондитер', 30000)],
                'stats': (1000, 500)}

    @staticmethod
    def get_logged(login, password):
        user = session.query(User).filter(User.email == login).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def get(user_id):
        return session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def new(surname, name, fathername, birth_year, birth_month, birth_day, age, email, password, sex, role='user'):
        user = User()
        user.surname = surname
        user.name = name
        user.age = age
        user.fathername = fathername
        user.birth_date = datetime.date(birth_year, birth_month, birth_day)
        user.sex = sex
        user.email = email
        user.role = role
        user.set_password(password)
        session.add(user)
        session.commit()


# ЭТО ЗАГЛУШКА НЕ УДАЛЯТЬ
class Model1(db.Model):
    __tablename__ = 'model1'
    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
