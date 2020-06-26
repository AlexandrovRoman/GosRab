from app import app, urls, config
from flask_migrate import MigrateCommand
from flask_script import Manager

manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def runserver():
    urls.register_blueprints()
    app.run(config.HOST, config.PORT)


manager.run()
