from app import db
import datetime
from utils.models import ModelMixin


class News(db.Model, ModelMixin):
    """ Контент новостной ленты сайта """

    id = db.Column(db.Integer,
                   primary_key=True, autoincrement=True)
    title = db.Column(db.String(40))
    preview = db.Column(db.String(80))
    description = db.Column(db.String)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    tags = db.Column(db.String, default="")  # Тэги новости через запятую
    image = db.Column(db.Binary, nullable=True)

    def __init__(self, title=None, preview=None, description=None, date=None, tags=None, image=None):
        super().__init__(title=title, preview=preview, description=description, date=date, tags=tags, image=image)

    def __repr__(self):
        return '<News {}>'.format(self.title)

    @classmethod
    def new(cls, title, preview, description, tags="", image_link=None, image=None):
        if not image:
            if image_link:
                with open(image_link, "rb") as f:
                    image = f.read()
        super().new(title, preview, description, tags=tags, image=image)
