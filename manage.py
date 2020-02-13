from os import makedirs
from os.path import exists
from app import app, add_urls
from flask_migrate import MigrateCommand
from flask_script import Manager
import users.models

"""
database-methods: https://flask-migrate.readthedocs.io/en/latest/
db init - начало поддержки миграций
db migrate - миграция бд
db upgrade - обновление бд
db downgrade - откат миграции
"""
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    add_urls()
    app.run()


@manager.option('-n', '--name', help='App name')
def startapp(name):
    if not exists(name):
        makedirs(name)
    open(f'{name}/views.py', 'w').close()
    with open(f'{name}/models.py') as f:
        f.write('from app import db\n')
    with open(f'{name}/urls') as f:
        f.writelines(['from utils.urls import path\n\n', 'urlpatterns = [\n', '    ', ']\n'])
    print("hello", name)


manager.run()
