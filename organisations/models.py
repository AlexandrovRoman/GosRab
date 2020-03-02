from app import db, session
from sqlalchemy import orm
from datetime import datetime
from users.models import User
from sqlalchemy.orm import relationship


class Organisation(db.Model):
    __tablename__ = 'organisations'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    creation_date = db.Column(db.Date, default=datetime.now)
    # personnel_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    users = relationship("User", backref='organisations')

    def __repr__(self):
        return f'<Organisation {self.name}>'

    @classmethod
    def new(cls, name, personnel_id=1, date=datetime.now):
        org = cls()
        org.name = name
        # org.personnel_id = personnel_id
        # org.personnel = session.query(User).filter(User.id == personnel_id).first()
        org.date = date
        session.add(org)
        session.commit()
