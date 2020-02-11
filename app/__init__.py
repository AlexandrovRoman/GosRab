from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask('__main__')
db = SQLAlchemy(app)


def init():
    from app import urls
    app.config.from_object(Config)
    migrate = Migrate(app, db)
