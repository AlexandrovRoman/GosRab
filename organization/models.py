from sqlalchemy.orm.exc import NoResultFound
from app import db
from datetime import datetime
from utils.models import ModelMixin
from utils.api import create_jwt


class Organization(db.Model, ModelMixin):
    """
    Организации на сайте.
    От имени организации имеется возможность создавать вакансии,
    принимать новых сотрудников на работу,
    вести учет сотрудников
    """

    name = db.Column(db.String(80), nullable=True)
    creation_date = db.Column(db.Date, default=datetime.now)
    personnel = db.relationship("User", backref='binded_org', lazy='select', foreign_keys="User.work_department_id")
    vacancies = db.relationship("Vacancy", back_populates='organization')
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship("User",
                            back_populates="organizations",
                            uselist=False,
                            foreign_keys="Organization.owner_id")
    org_type = db.Column(db.String)
    org_desc = db.Column(db.String)
    api_token = db.Column(db.String)

    def __init__(self,
                 name=None,
                 owner_id=None,
                 org_type=None,
                 org_desc=None,
                 date=None):
        super().__init__(name=name, owner_id=owner_id, org_desc=org_desc, org_type=org_type, creation_date=date)
        self.refresh_token()

    @classmethod
    def get_by_id(cls, user, org_id: int):
        """ Возвращает организацию по id, если пользователь является ее владельцем """

        try:
            return cls.get_by(id=org_id, owner_id=user.id)
        except NoResultFound:
            return

    @classmethod
    def new(cls, name, owner_id, org_type, org_desc, date=None):
        date = date if date else datetime.now()
        super().new(name, owner_id, org_type, org_desc, date)

    @property
    def required_workers(self):
        return list(filter(lambda vacancy: vacancy.worker_id is None, self.vacancies))

    @property
    def exists_workers(self):
        return list(filter(lambda vacancy: vacancy.worker_id is not None, self.vacancies))

    def refresh_token(self):
        """ Обновляет api токен организации """

        self.api_token = create_jwt(self.name)


class Vacancy(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    org_id = db.Column(db.Integer, db.ForeignKey('organization.id'))
    organization = db.relationship("Organization", back_populates="vacancies", uselist=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    salary = db.Column(db.Integer)
    title = db.Column(db.String)
    resume = db.relationship("Resume", backref='vacancy')

    def __init__(self,
                 org_id=None,
                 worker_id=None,
                 salary=None,
                 title=None):
        super().__init__(org_id=org_id, worker_id=worker_id, salary=salary, title=title)

    @classmethod
    def new(cls, org_id, worker_id, salary, title):
        super().new(org_id, worker_id, salary, title)

    def has_permission(self, user):
        return self.organization.owner == user or user in self.organization.personnel


class Resume(db.Model, ModelMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vacancy_id = db.Column(db.Integer, db.ForeignKey('vacancy.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    content = db.Column(db.String)
