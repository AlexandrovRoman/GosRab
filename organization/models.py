from app import db, session
from datetime import datetime
from app.models import base_new
from users.models import User


class Organization(db.Model):
    __tablename__ = 'organizations'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    creation_date = db.Column(db.Date, default=datetime.now)
    personnels = db.relationship("User", foreign_keys=[User.work_department_id], backref='binded_org', lazy='select')
    vacancies = db.relationship("Vacancy", backref='organization')
    owner_id = db.Column(db.Integer)
    org_type = db.Column(db.String)
    org_desc = db.Column(db.String)

    def __repr__(self):
        return f'<Organization {self.name}>'

    @classmethod
    def get_attached_to_personnel(cls, user):  # Возвращает организацию, к которой привязан кадровик
        return user.binded_org

    @classmethod
    def get_by_id(cls, user, org_id: int):  # Возвращает организацию под org_id,
        org = session.query(cls).get(org_id)
        if user.id != org.owner_id:  # если пользователь ею не владеет
            return None
        return org

    @classmethod
    def get_attached_to_user(cls, user):  # Возвращает организации, которыми обладает пользователь
        return session.query(cls).filter(cls.owner_id == user.id).all()

    @classmethod
    def new(cls, name, owner_id, org_type, org_desc, date=datetime.now):
        kwargs = {"name": name, "owner_id": owner_id, "org_desc": org_desc, "org_type": org_type, "date": date}
        base_new(cls, **kwargs)

    # def add_department(self, dep_name):
    #     department = Department(name=dep_name, organization=self)
    #     session.add(department)
    #     session.commit()

    # def add_hr_manager(self, user):
    #     user.add_roles(['hr manager'])
    #     self.hr_managers.append(user)

    # def add_user(self, new_user_id):  # добавляет пользователя в организацию
    #     user = session.query(User).filter(User.id == new_user_id).first()
    #     user.work_place_id = self.id

    def get_base_info(self):
        return self.id, self.name

    def get_full_info(self):
        return self.id, self.org_type, self.name, self.creation_date, self.org_desc, 'Путь к картинке'

    def get_required_workers(self):  # Список требуемых работников организации
        return [(vacancy.title, vacancy.salary) for vacancy in filter(lambda x: x.worker_id is None, self.vacancies)]

    def get_personnel(self):
        return [(hr.full_name, hr.salary, hr.id, bool(hr.t2_rel)) for hr in self.personnels]

    def get_workers(self):
        return [
            (vacancy.worker.full_name, vacancy.title, vacancy.salary, vacancy.worker.id, bool(vacancy.worker.t2_rel))
            for vacancy in filter(lambda x: x.worker_id is not None, self.vacancies)]

    # def delete_user(self, delete_user_id):  # удаляет пользователя из организации
    #     user = session.query(User).filter(User.id == delete_user_id).first()
    #     user.work_place_id = None


class Vacancy(db.Model):
    __tablename__ = 'vacancies'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organizations.id'))
    worker_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    salary = db.Column(db.Integer)
    title = db.Column(db.String)

    @classmethod
    def new(cls, org_id, worker_id, salary, title):
        kwargs = {
            'org_id': org_id,
            'worker_id': worker_id,
            'salary': salary,
            'title': title,
        }
        base_new(cls, **kwargs)

# class Department(db.Model):
#     __tablename__ = 'departments'
#
#     id = db.Column(db.Integer,
#                    primary_key=True, autoincrement=True)
#     name = db.Column(db.String(80), nullable=True)
#     organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True)
#     # employees = db.relationship("User", backref='work_department')
#
#     def __repr__(self):
#         return f'<Department {self.name} org: {self.organization.name} employees: {self.users}>'
