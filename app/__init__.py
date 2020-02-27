import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Session
from .config import Config
from .exceptions import UrlConnectError
from importlib import import_module

app = Flask('__main__')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init():
    global __factory

    if __factory:
        return

    conn_str = f'{config.BaseConfig.SQLALCHEMY_DATABASE_URI}?check_same_thread=False'
    if app.debug:
        print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    try:
        return __factory()
    except TypeError:
        global_init()
        return __factory()


login_manager = LoginManager()
login_manager.init_app(app)


def add_urls():
    for file in config.urlpatterns:
        import_module(file)
