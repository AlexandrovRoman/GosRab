from users.models import Role
from app import session

session.query(Role).delete()
Role.new('user', 'peasant')
Role.new('personnel', 'управляет кадрами организации')
Role.new('manager', 'может управлять организацией')
Role.new('admin', 'доступны фичи админа: .......')
Role.new('superuser', 'доступны фичи суперюзера: .........')
session.commit()
