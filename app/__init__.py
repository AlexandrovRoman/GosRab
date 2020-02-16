from warnings import warn
from flask import Flask, redirect, url_for
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .config import Config
import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

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

    conn_str = f'{config.BaseConfig.SQLALCHEMY_DATABASE_URI}?check_same_thread=False'
    if app.debug:
        print(f"Подключение к базе данных по адресу {conn_str}")

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()


login_manager = LoginManager()
login_manager.init_app(app)


class Roled:

    def is_accessible(self):
        roles_accepted = getattr(self, 'roles_accepted', None)
        if current_user.role in roles_accepted:
            return True
        else:
            return False

    def _handle_view(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next="/admin"))
        if not self.is_accessible():
            return redirect(url_for('/'))


class AdminView(Roled, ModelView):
    def __init__(self, *args, **kwargs):
        self.roles_accepted = kwargs.pop('roles_accepted', list())
        super().__init__(*args, **kwargs)


class NewsView(AdminView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StatisticView(AdminView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        return current_user.role in ['admin', 'superuser']

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/')


from users.models import *

admin = Admin(app, 'Главная страница', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(NewsView(model=Model1, session=db.session, name='Новости', roles_accepted=['admin']))
admin.add_view(NewsView(model=User, session=db.session, name='Статистика', roles_accepted=['superuser']))


def add_urls():
    from errors import views
    from app import urls
    if app.debug:
        if len(urls.urlpatterns) == 0:
            warn("urlpatterns is empty")
        assert all(urls.urlpatterns)
