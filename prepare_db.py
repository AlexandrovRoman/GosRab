import os
import shutil
import sys
from pprint import pprint

from news.models import News
from organization.models import Organization, Vacancy
from users.models import User, Course, T2Form
from utils.clear_postgresql_db import DB
from utils.excel_DB import export_from_excel
from app import config


def confirm(msg):
    ans = input(f'\n\t{msg}. Наберите "n", для выключения, enter для продолжения.')
    if ans == 'n':
        sys.exit()
    print()


def create_test_models():
    export_from_excel('test_models/orgs.xlsx', Organization.new)
    export_from_excel('test_models/users.xlsx', User.new)
    export_from_excel('test_models/t2.xlsx', T2Form.new)

    export_from_excel('test_models/vacancies.xlsx', Vacancy.new)
    export_from_excel('test_models/news.xlsx', News.new)
    export_from_excel('test_models/courses.xlsx', Course.new)


if os.path.exists('migrations'):
    shutil.rmtree('migrations')

db = DB(config.db, config.user, config.password, *config.url.split(":"))
db.clear_tables()
pprint(db.get_tables())

os.system(f'{sys.executable} manage.py db init')
confirm('manage.py db init завершено.')
os.system(f'{sys.executable} manage.py db migrate')
confirm('manage.py db migrate завершено.')
os.system(f'{sys.executable} manage.py db upgrade')
confirm('manage.py db upgrade завершено.')
create_test_models()
print('\n\texcel_DB.py завершено.\n')
