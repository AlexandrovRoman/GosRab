from app import db
import datetime


class News(db.Model):
    __tablename__ = 'news_table'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String, nullable=True)
    date = db.Column(db.DateTime,
                                     default=datetime.datetime.now)
    tags = db.Column(db.String, nullable=True) # Тэги новости через запятую

    def __repr__(self):
        return '<News {}>'.format(self.title)