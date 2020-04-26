import os
import shutil
import sys
from news.models import HotNews, News
from organization.models import Organization, Vacancy
from users.models import User, Course, T2Form
from utils.excel_DB import export_from_excel


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
    export_from_excel('test_models/hot_news.xlsx', HotNews.new)
    export_from_excel('test_models/news.xlsx', News.new)
    export_from_excel('test_models/courses.xlsx', Course.new)


if os.path.exists('migrations'):
    shutil.rmtree('migrations')

os.system(f'{sys.executable} manage.py db init')
confirm('manage.py db init завершено.')
os.system(f'{sys.executable} manage.py db migrate')
confirm('manage.py db migrate завершено.')
os.system(f'{sys.executable} manage.py db upgrade')
confirm('manage.py db upgrade завершено.')
create_test_models()
print('\n\texcel_DB.py завершено.\n')
