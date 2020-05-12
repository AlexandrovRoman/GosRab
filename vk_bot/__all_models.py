import sqlalchemy
from vk_bot.db_session import *


class BugReport(SqlAlchemyBase):
    __tablename__ = 'bug_reports'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.String)
    message = sqlalchemy.Column(sqlalchemy.String)

    def new(self, sender_id, date, message):
        session = create_session()
        bug_report = BugReport()
        bug_report.sender_id = sender_id
        bug_report.date = date
        bug_report.message = message
        session.add(bug_report)
        session.commit()
        return bug_report


class Comment(SqlAlchemyBase):
    __tablename__ = 'comments'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    sender_id = sqlalchemy.Column(sqlalchemy.Integer)
    date = sqlalchemy.Column(sqlalchemy.String)
    message = sqlalchemy.Column(sqlalchemy.String)

    def new(self, sender_id, date, message):
        session = create_session()
        comment = Comment()
        comment.sender_id = sender_id
        comment.date = date
        comment.message = message
        session.add(comment)
        session.commit()
        return comment
