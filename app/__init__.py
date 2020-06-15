from os import path
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from .config import Config

here = path.abspath(path.dirname(__file__))
app = Flask(__name__, template_folder=path.join(path.split(here)[0], "templates"),
            static_folder=path.join(path.split(here)[0], "static"))

app.config.from_object(Config)
db = SQLAlchemy(app)
session = db.session
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app, prefix='/api')
