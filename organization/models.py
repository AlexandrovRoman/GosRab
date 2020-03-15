from app import db, session
from datetime import datetime
from sqlalchemy.orm import relationship


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
    def new(cls, name, date=datetime.now):
        org = cls()
        org.name = name
        org.date = date
        session.add(org)
        session.commit()

    def add_department(self, dep_name):
        department = Department(name=dep_name, organization=self)
        session.add(department)
        session.commit()

    def add_hr_manager(self, user):
        user.add_roles(['hr manager'])
        self.hr_managers.append(user)


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
