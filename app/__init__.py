from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from .config import Config, template_folder, static_folder

app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app, prefix='/api')
