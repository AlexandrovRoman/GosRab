import datetime
import sqlalchemy
from vk_bot.db_session import *


class Message:
    @classmethod
    def new(cls, sender_id, message):
        session = create_session()
        obj = cls(sender_id=sender_id, message=message)
        session.add(obj)
        session.commit()
        return obj


class BugReport(SqlAlchemyBase, Message):
    __tablename__ = 'bug_reports'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)
    message = sqlalchemy.Column(sqlalchemy.String)


class Comment(SqlAlchemyBase, Message):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.utcnow)
    message = sqlalchemy.Column(sqlalchemy.String)
