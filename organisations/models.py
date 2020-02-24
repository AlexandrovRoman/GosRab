from app import db
from sqlalchemy import orm
from datetime import datetime


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