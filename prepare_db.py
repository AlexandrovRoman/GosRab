import os
import argparse
import sys
from news.models import HotNews, News
from organization.models import Organization
from users.models import User, Course
from utils.excel_DB import export_from_excel
from utils.set_roles import create_roles


def confirm(msg):
    ans = input(f'\n\t{msg}. Наберите "n", для выключения, enter для продолжения.')
    if ans == 'n':
        sys.exit()
    print()


def create_test_models():
    export_from_excel('test_models/orgs.xlsx', Organization.new)
    export_from_excel('test_models/users.xlsx', User.new)
    export_from_excel('test_models/hot_news.xlsx', HotNews.new)
    export_from_excel('test_models/news.xlsx', News.new)
    export_from_excel('test_models/courses.xlsx', Course.new)


parser = argparse.ArgumentParser()
parser.add_argument("pythonenv")

args = parser.parse_args()

os.system(f'{args.pythonenv} manage.py db init')
confirm('manage.py db init завершено.')
os.system(f'{args.pythonenv} manage.py db migrate')
confirm('manage.py db migrate завершено.')
os.system(f'{args.pythonenv} manage.py db upgrade')
confirm('manage.py db upgrade завершено.')
create_roles()
confirm('set_roles.py завершено.')
create_test_models()
print('\n\texcel_DB.py завершено.\n')