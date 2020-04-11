import datetime
from flask_login import UserMixin
from sqlalchemy import orm
from app import db, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import ModelMixin

roles_relationship = db.Table('roles_relationship',
                              db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                              db.Column('role_id', db.Integer, db.ForeignKey('roles.role_id')))


class User(db.Model, ModelMixin, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    t2_rel = orm.relation("T2Form", back_populates='linked_user')

    name = db.Column(db.String(80))
    surname = db.Column(db.String(80))
    fathername = db.Column(db.String(80), nullable=True)
    email = db.Column(db.String(40), index=True, unique=True)
    hashed_password = db.Column(db.String)
    birth_date = db.Column(db.Date)
    age = db.Column(db.Integer)  # TODO: Лишний параметр, стоит удалить
    sex = db.Column(db.String(7))
    marriage = db.Column(db.String(20))
    grate = db.Column(db.String, default='Новичок')
    education = db.Column(db.String, default='Отсутствует')
    foreign_languges = db.Column(db.String, default='Отсутствует')
    start_place = db.Column(db.String)
    nationality = db.Column(db.String)
    about_myself = db.Column(db.String, default='Отсутствует')
    # organization info
    post = db.Column(db.String, nullable=True)

    work_department_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True)
    salary = db.Column(db.Integer, nullable=True)

    roles = db.relationship('Role', secondary=roles_relationship, backref=db.backref('users', lazy='dynamic'))
    vacancies = db.relationship("Vacancy", backref='worker')

    def __init__(self,
                 name=None,
                 surname=None,
                 fathername=None,
                 email=None,
                 password=None,
                 binded_org=None,
                 salary=None,
                 birth_year=None,
                 birth_month=None,
                 birth_day=None,
                 sex=None,
                 marriage=None,
                 grate=None,
                 education=None,
                 foreign_languges=None,
                 start_place=None,
                 about_myself=None,
                 roles=("user",)):

        roles = " ".join(roles)
        self.__class__.add_roles(self, roles)

        kwargs = {
            "surname": surname,
            "name": name,
            "fathername": fathername,
            "work_department_id": binded_org,
            "salary": salary,
            "birth_date": datetime.date(birth_year, birth_month, birth_day),
            "age": (datetime.datetime.now() - datetime.datetime(birth_year, birth_month, birth_day)).days // 365,
            "email": email,
            "hashed_password": generate_password_hash(password),
            "sex": sex,
            "marriage": marriage,
            "grate": grate,
            "education": education,
            "foreign_languges": foreign_languges,
            "start_place": start_place,
            "about_myself": about_myself,
        }
        super().__init__(**kwargs)

    def __repr__(self):
        return f'<User {self.name}>'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    @property
    def full_name(self):
        return f'{self.surname} {self.name} {self.fathername}'

    @property
    def get_profile_info(self):
        return {'Surname': self.surname, 'Name': self.name, 'Middle_name': self.fathername,
                'Gender': self.sex, 'Age': self.age, 'Grade': self.grate,
                'Education': self.education, 'Marital_status': self.marriage,
                'Knowledge_of_foreign_language': self.foreign_languges, 'Email': self.email,
                'About_myself': self.about_myself, 'Workplace': 'Автосервис Михаил-авто(отдел продаж) - Глав.Менеджер'}

    @classmethod
    def get_logged(cls, login, password):
        user = cls.get_by(email=login)
        if user and user.check_password(password):
            return user
        return None

    @classmethod
    def get(cls, user_id):
        return cls.get_by(id=user_id)

    @classmethod
    def new(cls, surname, name, fathername, binded_org, salary, birth_year, birth_month, birth_day,
            age, email, password, sex, marriage):
        super().new(name, surname, fathername, email, password,
                    binded_org, salary, birth_year, birth_month, birth_day, sex, marriage=marriage)

    @staticmethod
    def add_roles(user, role_names):
        for role_name in role_names.split():
            role = Role.get_role_for_name(role_name)
            local_session_role = session.merge(role)
            user.roles.append(local_session_role)


class T2Form(db.Model, ModelMixin):
    __tablename__ = 't2'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    org_name_prop = db.Column(db.String)

    linked_user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    linked_user = orm.relation('User')

    compile_date = db.Column(db.Date, default=datetime.datetime.now())
    service_number = db.Column(db.Integer, default=55)
    taxpayer_id_number = db.Column(db.String, default='0123456789012')
    pension_insurance_certificate = db.Column(db.String, default='123-456-789 12')

    work_nature = db.Column(db.String, default='Постоянная')  # Характер работы
    work_kind = db.Column(db.String, default='Основная')  # Вид работы

    employment_contract_id = db.Column(db.Integer, default=0)
    employment_contract_date = db.Column(db.Date, default=datetime.datetime.now())

    birthdate = db.Column(db.Date, default=datetime.datetime.now())

    birthplace = db.Column(db.String)
    birthplace_okato = db.Column(db.String, default='42432712412')

    nationality = db.Column(db.String, default='Россия')
    nationality_okin = db.Column(db.String, default='1')

    foreign_language_knowledge = db.Column(db.String, default='Не имеет знаний иностраных языков')
    foreign_language_knowledge_okin = db.Column(db.String, default='016,017')
    education = db.Column(db.String, default='Среднее')
    education_okin = db.Column(db.String, default='07')

    education_list = db.Column(db.String, default='Отсутствует')  # Разделитель ;

    profession = db.Column(db.String, default='Маркетолог')
    profession_code = db.Column(db.String, default='23461')
    profession_other = db.Column(db.String, default='')
    profession_other_code = db.Column(db.String, default='')

    experience_checked = db.Column(db.Date, default=datetime.datetime.now())
    experience = db.Column(db.String, default='1,2,3,4,5,6,7,8,9,10,11,12')

    marriage_okin = db.Column(db.String, default='2')

    family = db.Column(db.String,
                       default='Отсутствует')
    passport_id = db.Column(db.String)
    passport_given = db.Column(db.Date, default=datetime.datetime.now())

    def __init__(self,
                 email=None,
                 password=None,
                 surname=None,
                 name=None,
                 fathername=None,
                 binded_org=None,
                 salary=None,
                 marriage=None,
                 gender=None,
                 org_name=None,
                 compile_date=None,
                 service_number=None,
                 taxpayer_id_number=None,
                 pension_insurance_certificate=None,
                 work_nature=None,
                 work_kind=None,
                 employment_contract_id=None,
                 employment_contract_date=None,
                 birthdate=None,
                 birthplace=None,
                 birthplace_okato=None,
                 nationality=None,
                 nationality_okin=None,
                 foreign_language_knowledge=None,
                 foreign_language_knowledge_okin=None,
                 education=None,
                 education_okin=None,
                 education_list=None,
                 profession=None,
                 profession_code=None,
                 profession_other=None,
                 profession_other_code=None,
                 experience_checked=None,
                 experience=None,
                 marriage_okin=None,
                 family=None,
                 passport_id=None,
                 passport_given=None):
        linked_user = User.get_by(email=email)

        if linked_user is None:
            linked_user = User(name, surname, fathername, email, password, binded_org, salary,
                               birthdate.year, birthdate.month, birthdate.day, gender, marriage)
            linked_user.save()
            print('На основе Т2 создан пользователь', linked_user.full_name)

        kwargs = {
            'org_name_prop': org_name,
            'linked_user_id': linked_user.id,
            'compile_date': compile_date,
            'service_number': service_number,
            'taxpayer_id_number': taxpayer_id_number,
            'pension_insurance_certificate': pension_insurance_certificate,
            'work_nature': work_nature,
            'work_kind': work_kind,
            'employment_contract_id': employment_contract_id,
            'employment_contract_date': employment_contract_date,
            'birthdate': birthdate,
            'birthplace': birthplace,
            'birthplace_okato': birthplace_okato,
            'nationality': nationality,
            'nationality_okin': nationality_okin,
            'foreign_language_knowledge': foreign_language_knowledge,
            'foreign_language_knowledge_okin': foreign_language_knowledge_okin,
            'education': education,
            'education_okin': education_okin,
            'education_list': education_list,
            'profession': profession,
            'profession_code': profession_code,
            'profession_other': profession_other,
            'profession_other_code': profession_other_code,
            'experience_checked': experience_checked,
            'experience': experience,
            'marriage_okin': marriage_okin,
            'family': family,
            'passport_id': passport_id,
            'passport_given': passport_given
        }
        super().__init__(**kwargs)

    @classmethod
    def new(cls,
            email,
            password,
            surname,
            name,
            fathername,
            binded_org,
            salary,
            marriage,
            gender,
            org_name,
            compile_date,
            service_number,
            taxpayer_id_number,
            pension_insurance_certificate,
            work_nature,
            work_kind,
            employment_contract_id,
            employment_contract_date,
            birthdate,
            birthplace,
            birthplace_okato,
            nationality,
            nationality_okin,
            foreign_language_knowledge,
            foreign_language_knowledge_okin,
            education,
            education_okin,
            education_list,
            profession,
            profession_code,
            profession_other,
            profession_other_code,
            experience_checked,
            experience,
            marriage_okin,
            family,
            passport_id,
            passport_given):
        super().new(email, password, surname, name, fathername, binded_org, salary, marriage, gender, org_name,
                    compile_date, service_number, taxpayer_id_number, pension_insurance_certificate,
                    work_nature, work_kind, employment_contract_id, employment_contract_date, birthdate, birthplace,
                    birthplace_okato, nationality, nationality_okin, foreign_language_knowledge,
                    foreign_language_knowledge_okin, education, education_okin, education_list, profession,
                    profession_code, profession_other, profession_other_code, experience_checked,
                    experience, marriage_okin, family, passport_id, passport_given)

    @property
    def org_name(self):
        return self.org_name_prop

    @property
    def alphabet(self):
        return self.linked_user.surname[0]


class Role(db.Model, ModelMixin):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer,
                        primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(20), unique=True)
    description = db.Column(db.String(200))

    def __init__(self,
                 role_name=None,
                 description=None):
        super().__init__(role_name=role_name, description=description)

    @classmethod
    def new(cls, name, description):
        super().new(name, description)

    def __repr__(self):
        return f'<Role {self.role_name}, Возможности: {self.description}>'

    @classmethod
    def get_role_for_name(cls, role_name):
        return super().get_by(role_name=role_name)


class Course(db.Model, ModelMixin):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    course_type = db.Column(db.String(20))
    course_name = db.Column(db.String(70))
    data = db.Column(db.String(20))  # TODO: сделать в формате начало - конец
    description = db.Column(db.String)
    image = db.Column(db.String(20))  # TODO: хранить картинку в юазе данных

    def __init__(self,
                 course_type=None,
                 course_name=None,
                 data=None,
                 description=None,
                 image=None):
        super().__init__(course_type=course_type, course_name=course_name,
                         data=data, description=description, image=image)

    @classmethod
    def new(cls, course_type, name, data, description, image):
        super().new(course_type, name, data, description, image)

    @classmethod
    def get_courses(cls):
        courses = [(obj.course_type, obj.course_name, obj.data, obj.description, obj.image) for obj in cls.query.all()]
        return courses


# ЭТО ЗАГЛУШКА НЕ УДАЛЯТЬ
class Model1(db.Model):
    __tablename__ = 'model1'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
