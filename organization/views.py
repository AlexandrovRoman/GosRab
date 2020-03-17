from flask import render_template, request
from flask_login import current_user

from app import session
from organization.models import Organization


def organizations():
    orgs = Organization.get_attached_to_user(current_user)
    org_list = [org.get_full_info() for org in orgs]

    return render_template("organization/organizations.html", orgs=org_list)


def add_organization():
    return render_template("organization/add_organization.html")


def menu_organization():
    org_id = request.args.get('org_id')
    if not org_id.isdigit():
        return 'org_id должен быть числом'
    org = Organization.get_by_id(current_user, int(org_id))
    if org is None:
        return 'Нет доступа'

    org_info = org.get_full_info()

    return render_template("organization/menu_organization.html", org=org_info)


def personnel_department():
    org_id = request.args.get('org_id')
    if not org_id.isdigit():
        return 'org_id должен быть числом'
    org = Organization.get_by_id(current_user, int(org_id))
    if org is None:
        return 'Нет доступа'

    organization_info = {
        'desc': org.get_base_info(),
        'personnel': org.get_personnel(),
        'workers': org.get_workers(),
        'required_workers': org.get_required_workers(),
    }

    return render_template("personnel_department.html", **organization_info, len=len)


def job():
    jobs = [
        ('Хлебобулочный комбинат', 'Кондитер', 30000),
        ('Хлебобулочный комбинат', 'Директор', 50000),
        ('ПФР промю района', 'Администратор', 25000),
        ('ПФР промю района', 'Сис.Админ', 27500),
        ('Автосервис Михаил - авто', 'Механик', 27500),
        ('Автосервис Михаил - авто', 'Маляр', 33000),
        ('Автосервис Михаил - авто', 'Главный механик', 35000),
    ]
    return render_template("organization/job.html", jobs=enumerate(jobs, 1))

#
# def organization():
#     organization_info = current_user.get_organization(request.args.get('organization'))
#     if organization_info is None:
#         return 'Нет доступа'
#     return render_template("organization/organization.html", **organization_info)
