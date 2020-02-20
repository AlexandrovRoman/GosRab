from flask_admin import Admin
from app import db, app
from .models import *
from users.models import Model1, User

admin = Admin(app, 'Главная страница', url='/', index_view=HomeAdminView(name='Home'))
admin.add_view(NewsView(model=Model1, session=db.session, name='Новости', roles_accepted=['admin']))
admin.add_view(NewsView(model=User, session=db.session, name='Статистика', roles_accepted=['superuser']))
