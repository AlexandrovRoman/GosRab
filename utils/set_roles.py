from users.models import Role
from app import session


def create_roles():
    try:
        session.query(Role).delete()
    except:
        pass
    Role.new('user', 'peasant')
    Role.new('hr manager', 'управляет кадрами организации')
    Role.new('company director', 'может управлять организацией, создавать отделы')
    Role.new('head of department', 'глава отдела')
    Role.new('admin', 'доступны фичи админа: .......')
    Role.new('superuser', 'доступны фичи суперюзера: .........')
