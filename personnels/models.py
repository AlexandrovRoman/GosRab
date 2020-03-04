from app import db, session
from datetime import datetime
from sqlalchemy.orm import relationship, backref


class Personnel(db.Model):
    __tablename__ = 'personnel'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User", backref=backref("personnel", uselist=False))
    command_users = relationship("User", backref='personnel')

    def __repr__(self):
        return f'<Personnel {self.user.name}>'


    @classmethod
    def new(cls, id):
        pers = cls()
        pers.user_id = id
        session.add(pers)
        session.commit()