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
        return f'<Organization {self.name}>'

    @classmethod
    def get_attached_to_personnel(cls, user):  # Возвращает организацию, к которой привязан кадровик
        return session.query(cls).filter(cls.id == user.work_place_id).first()

    @classmethod
    def get_by_id(cls, user, org_id: int):  # Возвращает организацию под org_id,
        org = session.query(cls).filter(cls.id == org_id).first()
        if False:  # todo если пользователь ею не владеет
            return None
        return org

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

    def add_user(self, new_user_id):  # добавляет пользователя в организацию
        user = session.query(User).filter(User.id == new_user_id).first()
        user.work_place_id = self.id

    def get_base_info(self):
        return self.id, self.name

    def get_full_info(self):
        return self.id, 'Не поддерживается тип организаций', self.name, self.creation_date, 'Описание', 'Путь к картинке'

    def get_required_workers(self):  # todo Добавить список требуемых работников организации
        return [
            ('Механик', 30000),
        ]

    def get_personnel(self):
        return [(hr.surname + hr.name + hr.fathername,
                 hr.salary, hr.id) for hr in self.hr_managers]

    def get_workers(self):
        return [(worker.surname + worker.name + worker.fathername, worker.post,
                 worker.salary, worker.id) for worker in self.employees]

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
