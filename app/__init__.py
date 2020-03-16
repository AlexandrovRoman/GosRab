import sqlalchemy.ext.declarative as dec
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_dj.app_init import create_session
from .config import Config

app = Flask('__main__')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

SqlAlchemyBase = dec.declarative_base()

login_manager = LoginManager()
login_manager.init_app(app)
session = create_session(Config.SQLALCHEMY_DATABASE_URI, SqlAlchemyBase)
