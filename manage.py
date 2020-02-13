from os import makedirs
from os.path import exists
from app import app, add_urls
from flask_migrate import MigrateCommand
from flask_script import Manager
from app.config import models
from importlib import import_module

"""
database-methods: https://flask-migrate.readthedocs.io/en/latest/
db init - начало поддержки миграций
db migrate - миграция бд
db upgrade - обновление бд
db downgrade - откат миграции
some methods:
runserver - запуск сервера
startapp -n=name - создание приложения name
"""
manager = Manager(app)
manager.add_command('db', MigrateCommand)
for file in models:
    import_module(file)


@manager.command
def runserver():
    add_urls()
    app.run()


@manager.option('-n', '--name', help='App name')
def startapp(name):
    if not name:
        raise NameError
    if not exists(name):
        makedirs(name)
    open(f'{name}/views.py', 'w').close()
    with open(f'{name}/models.py', 'w') as f:
        f.write('from app import db\n')
    with open(f'{name}/urls.py', 'w') as f:
        f.writelines(['from utils.urls import path\n\n', 'urlpatterns = [\n', '    ', '\n]\n'])
    print(f'app {name} created')


manager.run()
