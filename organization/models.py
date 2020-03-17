from app import db, session
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models import base_new
from users.models import User


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    creation_date = db.Column(db.Date, default=datetime.now)
    employees = relationship("User", backref='work_place')
    departments = relationship("Department", backref='organization')
    hr_managers = relationship("User", backref='hr_department')

    def __repr__(self):
        return f'<Organisation {self.name}>'

    @classmethod
    def get_attached_to_personnel(cls, user):  # todo Вернуть организацию, к которой привязан кадровик
        return session.query(cls).all().pop()

    @classmethod
    def get_by_id(cls, user, org_id: int):  # todo Вернуть организацию под org_id,
        if False:  # todo если пользователь ею не владеет
            return None
        return session.query(cls).all().pop()

    @classmethod
    def get_attached_to_user(cls, user):  # todo Вернуть организации, которыми обладает пользователь
        return session.query(cls).all()

    @classmethod
    def new(cls, name, date=datetime.now):
        kwargs = {"name": name, "date": date}
        base_new(cls, **kwargs)

    def add_department(self, dep_name):
        department = Department(name=dep_name, organization=self)
        session.add(department)
        session.commit()

    def add_hr_manager(self, user):
        user.add_roles(['hr manager'])
        self.hr_managers.append(user)

    def add_user(self, new_user_id):  # добавляет пользователя в организацию\
        user = session.query(User).filter(User.id == new_user_id).first()
        user.work_place_id = self.id

    def get_base_info(self):  # id, название
        return 1, 'Автосервис Михаил-авто'

    def get_full_info(self):  # id, название
        return 1, 'ИП', 'Автосервис Михаил-авто', 'Ноябрь 2018', \
               'Тех. обслуживание; проверка авто перед покупкой; ремонтнык работы любой сложности.', 'Путь к картинке'

    def get_required_workers(self):
        return [
            ('Механик', 30000),  # Должность, Зарплата
        ]

    def get_personnel(self):
        return [
            ('Васильев Оливер Юхимович', 25000, -1),  # ФИО, Зарплата, user_id
            ('Мамонтов Данила Михайлович', 26000, -1),
        ]

    def get_workers(self):
        return [
            ('Федункив Сава Богданович', 'Управляющий', 30000, -1),  # ФИО, Должность, Зарплата, user_id
            ('Бирюков Мирослав Васильевич', 'Главный механик', 35000, -1),
        ]

    def delete_user(self, delete_user_id):  # удаляет пользователя из организации
        user = session.query(User).filter(User.id == delete_user_id).first()
        user.work_place_id = None


class Department(db.Model):
    __tablename__ = 'departments'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True)
    employees = relationship("User", backref='work_department')
    head_of_department = relationship("User", backref='subordinate_department', uselist=False)

    def __repr__(self):
        return f'<Department {self.name} org: {self.organization.name} employees: {self.users}>'

    def add_head_of_department(self, user):
        user.add_roles(['head of department'])
        self.head_of_department.append(user)
