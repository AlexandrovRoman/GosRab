from app import db
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models import base_new


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
        kwargs = {"name": name, "date": date}
        base_new(cls, **kwargs)
