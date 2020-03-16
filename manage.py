from Flask_DJ import manage
from Flask_DJ.app_init import add_urls
from app import app, config

"""database-methods: https://flask-migrate.readthedocs.io/en/latest/
db init - начало поддержки миграций
db migrate - миграция бды
db upgrade - обновление бд
db downgrade - откат миграции
some methods:
runserver - запуск сервера
startapp name - создание приложения name
new_user_has_full_data surname, name, fathername, birth_year, birth_month, birth_day, age, email, password, sex - 
создание пользователя с заданными параметрами
new_default_user mail, password - создание пользователя с дефолтными параметрами
"""


# Кто удалит - у того рак яичка
# https://getbootstrap.com/2.3.2/components

manage.init_manage_and_app(app)
manage.init_db_commands(config.models)

manage.manager.option("--templates", "-t", action="store_true")(
    manage.manager.option("--static", "-st", action="store_true")(
        manage.manager.option("name")(manage.startapp)))


@manage.manager.command
def runserver():
    add_urls(config.urlpatterns)
    manage.runserver(config.HOST, config.PORT)


manage.manager.run()
