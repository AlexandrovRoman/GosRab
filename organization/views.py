from flask import render_template, request
from flask_login import current_user


def organizations():
    orgs = current_user.get_organization_list()

    return render_template("organization/organizations.html", orgs=orgs)


def add_organization():
    return render_template("organization/add_organization.html")


def menu_organization():
    organization_info = current_user.get_organization(request.args.get('org_id'))
    if organization_info is None:
        return 'Нет доступа'

    return render_template("organization/menu_organization.html", org=organization_info)


def personnel_department():
    organization_info = current_user.get_organization_department(request.args.get('org_id'))
    if organization_info is None:
        return 'Нет доступа'

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


def organization():
    organization_info = current_user.get_organization(request.args.get('organization'))
    if organization_info is None:
        return 'Нет доступа'
    return render_template("organization/organization.html", **organization_info)
