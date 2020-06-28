from app import app, urls, config
from flask_migrate import MigrateCommand
from flask_script import Manager
from utils.excel_DB import export_from_excel

manager = Manager(app)
manager.add_command('db', MigrateCommand)
urls.register_blueprints()


@manager.command
def runserver():
    app.run(config.HOST, config.PORT)


@manager.command
def create_test_models():
    from users.models import User, Course, T2Form
    from news.models import News
    from organization.models import Organization, Vacancy
    export_from_excel('test_models/orgs.xlsx', Organization.new)
    export_from_excel('test_models/users.xlsx', User.new)
    export_from_excel('test_models/t2.xlsx', T2Form.new)

    export_from_excel('test_models/vacancies.xlsx', Vacancy.new)
    export_from_excel('test_models/news.xlsx', News.new)
    export_from_excel('test_models/courses.xlsx', Course.new)


if __name__ == '__main__':
    manager.run()
