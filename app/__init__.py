from warnings import warn
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

app = Flask('__main__')
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

SqlAlchemyBase = dec.declarative_base()
__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("Необходимо указать файл базы данных.")

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


login_manager = LoginManager()
login_manager.init_app(app)


def add_urls():
    from app import urls
    from errors import views
    if len(urls.urlpatterns) == 0:
        warn("urlpatterns is empty")
    assert all(urls.urlpatterns)
