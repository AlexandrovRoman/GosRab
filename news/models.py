from app import db
import datetime
from app.models import ModelMixin


class HotNews(db.Model, ModelMixin):
    __tablename__ = 'hot_news'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String, nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    tags = db.Column(db.String, nullable=True)  # Тэги новости через запятую
    link = db.Column(db.String, default='#')

    def __init__(self, title=None, description=None, date=None, tags=None, link=None):
        super().__init__(title=title, description=description, date=date, tags=tags, link=link)

    def __repr__(self):
        return '<News {}>'.format(self.title)

    @classmethod
    def get_news(cls):
        news = [(obj.title, obj.description, obj.link) for obj in cls.query.all()]
        return news

    @classmethod
    def new(cls, title, description, link='#'):
        super().new(title, description, link=link)


class News(db.Model, ModelMixin):
    __tablename__ = 'news'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String, nullable=True)
    image_link = db.Column(db.String, nullable=True)

    def __init__(self, title=None, description=None, image_link=None):
        super().__init__(title=title, description=description, image_link=image_link)

    def __repr__(self):
        return '<News {}>'.format(self.title)

    @classmethod
    def get_courses(cls):
        courses = [(obj.title, obj.description, obj.image_link) for obj in cls.query.all()]
        return courses

    @classmethod
    def new(cls, title, description, image_link):
        super().new(title, description, image_link)
