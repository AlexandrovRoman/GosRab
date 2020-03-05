from app import db, session
from datetime import datetime
from sqlalchemy.orm import relationship


class Organization(db.Model):
    __tablename__ = 'organization'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=True)
    creation_date = db.Column(db.Date, default=datetime.now)
    users = relationship("User", backref='organization')

    def __repr__(self):
        return f'<Organisation {self.name}>'

    @classmethod
    def new(cls, name, date=datetime.now):
        org = cls()
        org.name = name
        org.date = date
        session.add(org)
        session.commit()
