from warnings import warn
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config

app = Flask('__main__')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def add_urls():
    from app import urls
    if len(urls.urlpatterns) == 0:
        warn("urlpatterns is empty")
    assert all(urls.urlpatterns)
