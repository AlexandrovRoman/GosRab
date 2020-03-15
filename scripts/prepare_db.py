import os
import argparse
import sys


def confirm(msg):
    ans = input(f'\n\t{msg}. Наберите "n", для выключения, enter для продолжения.')
    if ans == 'n':
        sys.exit()
    print()
    
    
parser = argparse.ArgumentParser()
parser.add_argument("pythonenv")

args = parser.parse_args()

os.system(f'{args.pythonenv} manage.py db init')
confirm('manage.py db init завершено.')
os.system(f'{args.pythonenv} manage.py db migrate')
confirm('manage.py db migrate завершено.')
os.system(f'{args.pythonenv} manage.py db upgrade')
confirm('manage.py db upgrade завершено.')
os.system(f'{args.pythonenv} scripts/set_roles.py')
confirm('set_roles.py завершено.')
os.system(f'{args.pythonenv} excel-DB.py')
print('\n\texcel-DB.py завершено.\n')
