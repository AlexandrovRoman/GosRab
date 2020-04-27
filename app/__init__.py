import sqlalchemy.ext.declarative as dec
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_dj.app_init import create_session, db_init
from flask_restful import Api
from .config import Config
from rest_API import UserListResource, UserResource
from os import path

here = path.abspath(path.dirname(__file__))
app = Flask(__name__, template_folder=path.join(path.split(here)[0], "templates"),
            static_folder=path.join(path.split(here)[0], "static"))

api = Api(app)
# Куда девать API URLы?
api.add_resource(UserListResource, '/api/user')
api.add_resource(UserResource, '/api/v2/user/<int:user_id>')

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

SqlAlchemyBase = dec.declarative_base()

login_manager = LoginManager()
login_manager.init_app(app)
db_init(Config.SQLALCHEMY_DATABASE_URI, SqlAlchemyBase, None)
session = create_session()
