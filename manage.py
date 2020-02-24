from os import makedirs
from os.path import exists
from app import app, add_urls, global_init
from flask_migrate import MigrateCommand
from flask_script import Manager
from app.config import models
from importlib import import_module
from users.views import user_add
import sys

"""database-methods: https://flask-migrate.readthedocs.io/en/latest/
db init - начало поддержки миграций
db migrate - миграция бд
db upgrade - обновление бд
db downgrade - откат миграции
some methods:
runserver - запуск сервера
startapp name - создание приложения name
new_user_has_full_data surname, name, fathername, birth_year, birth_month, birth_day, age, email, password, sex - 
создание пользователя с заданными параметрами
new_default_user mail, password - создание пользователя с дефолтными параметрами
"""
manager = Manager(app)
manager.add_command('db', MigrateCommand)
for file in models:
    import_module(file)

global_init('app.db')

# Кто удалит - у того рак яичка
# https://getbootstrap.com/2.3.2/components

@manager.command
def new_user_has_full_data(surname, name, fathername, birth_year, birth_month, birth_day, age, email, password, sex):
    user_add(surname, name, fathername, birth_year, birth_month, birth_day, age, email, password, sex)


@manager.command
def new_default_user(mail, password):
    user_add('Олегов', 'Исач', 'Олегович', 2000, 3, 15, 10, mail, password, 'М')


@manager.command
def runserver():
    add_urls()
    app.run()


@manager.command
def startapp(name):
    if not exists(name):
        makedirs(name)
    with open(f'{name}/views.py', 'w') as f:
        f.write('# Create your views functions or classes\n')
    with open(f'{name}/models.py', 'w') as f:
        f.write('from app import db\n\n# Create your models\n')
    with open(f'{name}/urls.py', 'w') as f:
        f.write('from utils.urls import path\n\n# Add your urls\nurlpatterns = [\n    \n]\n')
    with open(f'{name}/forms.py', 'w') as f:
        f.write('from flask_wtf import FlaskForm\nimport wtforms\n\n# Create your forms\n')
    print(f'app {name} created')


manager.run()
