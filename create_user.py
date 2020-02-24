from app import app, global_init
from flask_migrate import MigrateCommand
from flask_script import Manager
from app.config import models
from importlib import import_module
from users.views import user_add

manager = Manager(app)
manager.add_command('db', MigrateCommand)
for file in models:
    import_module(file)

global_init('app.db')

user_add('Олегов', 'Исач', 'Олегович', 2000, 3, 15, 10, 'example@email.ru', 'qwertyuiop', 'Мужской', 'admin')