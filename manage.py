from flask_dj import manage
from flask_dj.app_init import add_urls
from app import app, config

"""database-methods: https://flask-migrate.readthedocs.io/en/latest/
db init - начало поддержки миграций
db migrate - миграция бды
db upgrade - обновление бд
db downgrade - откат миграции
some methods:
runserver - запуск сервера
startapp name - создание приложения name, возможно создания папки приложения с помощью флагов -t и -st
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
    if not app.debug:
        print(f"Correct url: http://{config.HOST}:{config.PORT}/")
    manage.runserver(config.HOST, config.PORT)


manage.manager.run()
