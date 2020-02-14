from os import makedirs
from os.path import exists
from app import app, add_urls
from flask_migrate import MigrateCommand
from flask_script import Manager
from app.config import models
from importlib import import_module
from app import global_init
from users.views import user_add

"""
database-methods: https://flask-migrate.readthedocs.io/en/latest/
db init - начало поддержки миграций
db migrate - миграция бд
db upgrade - обновление бд
db downgrade - откат миграции
some methods:
runserver - запуск сервера
startapp name - создание приложения name
db downgrade - 
runserver - запоткат миграции
some methods:уск сервера
startapp -n=name - создание приложения name
"""
manager = Manager(app)
manager.add_command('db', MigrateCommand)
for file in models:
    import_module(file)

global_init('app.db')
user_add('Олегов', 'Исач', 'Олегович', 2000, 3, 15, 10, 'example@email.ru', 'qwertyuiop', 'М')
@manager.command
def runserver():
    add_urls()
    app.run()


@manager.command
@manager.option('-n', '--name', help='App name')
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
