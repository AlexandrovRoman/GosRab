from app import db, create_session
import datetime


session = create_session()


class News(db.Model):
    __tablename__ = 'news_table'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String, nullable=True)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    tags = db.Column(db.String, nullable=True)  # Тэги новости через запятую
    link = db.Column(db.String, default='#')

    def __repr__(self):
        return '<News {}>'.format(self.title)

    @staticmethod
    def get_news():
        news = [(obj.id, obj.title, obj.description, obj.link) for obj in News.query.all()]
        return news

    @staticmethod
    def new(title, description, link='#'):
        news = News()
        news.title = title
        news.description = description
        news.link = link
        session.add(news)
        session.commit()


class Courses:
    __tablename__ = 'courses_table'

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=True)
    description = db.Column(db.String, nullable=True)
    image_link = db.Column(db.String, nullable=True)

    def __repr__(self):
        return '<News {}>'.format(self.title)

    @staticmethod
    def get_courses():
        courses = [(obj.id, obj.title, obj.description, obj.image_link) for obj in News.query.all()]
        return courses

    @staticmethod
    def new(title, description, image_link):
        course = Courses()
        course.title = title
        course.description = description
        course.image_link = image_link
        session.add(course)
        session.commit()
