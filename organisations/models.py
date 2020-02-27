from app import db, create_session
from sqlalchemy import orm
from datetime import datetime
from users.models import User

session = create_session()


class Organisation(db.Model):
    __tablename__ = 'organisation'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    creation_date = db.Column(db.Date, default=datetime.now)
    personnel_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    personnel = orm.relation('User')

    def __repr__(self):
        return f'<Organisation {self.name}>'

    @classmethod
    def new(cls, name, personnel_id, date=datetime.now):
        org = cls()
        org.name = name
        org.personnel_id = personnel_id
        org.personnel = session.query(User).filter(User.id == personnel_id).first()
        org.date = date
        session.add(org)
        session.commit()
