from flask import render_template, request, make_response, redirect, url_for
from flask_login import current_user

def organizations():
    return render_template("organizations.html")

def add_organization():
    return render_template("add_organization.html")

def menu_organization():
    return render_template("menu_organization.html")

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
    return render_template("users/job.html", jobs=enumerate(jobs, 1))

def organization():
    organization_info = current_user.get_organization(request.args.get('organization'))
    if organization_info is None:
        return 'Нет доступа'
    return render_template("users/organization.html", **organization_info)