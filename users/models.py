import datetime
from flask_login import UserMixin
from app import db, session
from werkzeug.security import generate_password_hash, check_password_hash

roles_relationship = db.Table('roles_relationship',
                 db.Column('user_id', db.Integer, db.ForeignKey('users_list.id')),
                 db.Column('role_id', db.Integer, db.ForeignKey('roles_list.role_id')))


class User(db.Model, UserMixin):
    __tablename__ = 'users_list'

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
    sex = db.Column(db.String(7), nullable=True)  # М/Ж
    grate = db.Column(db.String, default='Новичок')
    education = db.Column(db.String, default='Отсутствует')
    foreign_languges = db.Column(db.String, default='Отсутствует')
    start_place = db.Column(db.String)
    nationality = db.Column(db.String)
    marriage = db.Column(db.String(20))
    about_myself = db.Column(db.String, default='Отсутствует')
    organization_foreign_id = db.Column(db.Integer, db.ForeignKey('organization.id'), nullable=True)
    roles = db.relationship('Role', secondary=roles_relationship, backref=db.backref('users', lazy='dynamic'))
    # personnel_foreign_id = db.Column(db.Integer, db.ForeignKey('personnel.id'), nullable=True)

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
                'About_myself': self.about_myself}

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
    def new(surname, name, fathername, birth_year, birth_month, birth_day,
            age, email, password, sex, marriage, org_id, roles='user'):
        user = User()
        user.surname = surname
        user.name = name
        user.age = age
        user.fathername = fathername
        user.birth_date = datetime.date(birth_year, birth_month, birth_day)
        user.sex = sex
        user.email = email
        user.marriage = marriage
        user.set_password(password)
        user.organization_foreign_id = org_id
        User.add_roles(user, roles)
        session.add(user)
        session.commit()


    @staticmethod
    def add_roles(user, role_names):
        for role_name in role_names.split():
            role = Role.query.filter_by(role_name=role_name).first()
            local_session_role = session.merge(role)
            user.roles.append(local_session_role)
        session.commit()


class Role(db.Model):
    __tablename__ = 'roles_list'

    role_id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(200))

    @staticmethod
    def new(name, description):
        role = Role()
        role.role_name = name
        role.description = description
        session.add(role)
        session.commit()

    def __repr__(self):
        return '<Role {}, Возможности:{}>'.format(self.role_name, self.description)


# ЭТО ЗАГЛУШКА НЕ УДАЛЯТЬ
class Model1(db.Model):
    __tablename__ = 'model1'
    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
