import datetime

from flask import render_template, request, redirect
from flask_login import current_user, login_required
from app import session
from organization.forms import AddOrganizationForm, SendResumeForm
from organization.models import Organization, Vacancy, Resume
from users.utils import check_confirmed


@login_required
@check_confirmed
def organizations():
    user_orgs = Organization.get_attached_to_user(current_user)

    return render_template("organization/organizations.html", orgs=user_orgs)


@login_required
@check_confirmed
def add_organization():
    form = AddOrganizationForm()
    if form.validate_on_submit():
        org = Organization(
            date=datetime.datetime.now().date(),
            name=form.name.data,
            org_type=form.org_type.data,
            org_desc=form.org_desc.data,
            owner_id=current_user.id
        )
        org.save(add=True)
        return redirect('/organization/profile/organizations/')

    return render_template("organization/add_organization.html", form=form)


@login_required
@check_confirmed
def send_resume(vacancy_id):
    vacancy = Vacancy.query.filter_by(id=vacancy_id).first_or_404()
    if vacancy.worker_id is not None:
        return 'Должность занята'
    form = SendResumeForm()
    if form.validate_on_submit():
        resume = Resume(
            title=form.contents.data,
            user_id=current_user.id,
            vacancy_id=vacancy_id,
        )
        resume.save(add=True)
        return redirect('/organization//job')

    return render_template("organization/send_resume.html", form=form)


@login_required
@check_confirmed
def menu_organization():
    org_id = request.args.get('org_id')
    if not org_id.isdigit():
        return 'org_id должен быть числом'
    org = Organization.get_by_id(current_user, int(org_id))
    if org is None:
        return 'Нет доступа'

    return render_template("organization/menu_organization.html", org=org)


@login_required
@check_confirmed
def personnel_department():
    org_id = request.args.get('org_id')
    if not org_id.isdigit():
        return 'org_id должен быть числом'
    org = Organization.get_by_id(current_user, int(org_id))
    if org is None:
        return 'Нет доступа'
    if request.method == 'POST':
        Vacancy(org_id=int(org_id), salary=request.form['salary'], title=request.form['title']).save()

    organization_info = {
        'org': org,
        'personnel': org.personnels,
        'workers': org.get_workers(),
        'required_workers': org.get_required_workers(),
    }

    return render_template("personnel_department.html", **organization_info, len=len)


@login_required
@check_confirmed
def show_pretenders(vacancy_id):
    vacancy = Vacancy.query.filter_by(id=vacancy_id).first_or_404()
    if vacancy.has_permission(current_user):
        return render_template('organization/show_pretenders.html', vacancy=vacancy)
    return 'Вы не являетесь владельцем вакансии'


@login_required
@check_confirmed
def hire_worker(resume_id):
    resume = session.query(Resume).get(resume_id)
    if not resume:
        return 'Резюме отсутствует'
    vacancy = resume.vacancy
    if vacancy.has_permission(current_user):
        for r in vacancy.resume:
            if r.id != resume_id:
                pass  # Выслать письма об отказе в пользу другого
            r.delete()
        vacancy.worker_id = resume.user_id
        vacancy.save()
        # Выслать письмо об принятии на должность
        return redirect('/organization/profile/organizations/')
    return 'Вы не являетесь владельцем вакансии'


def job():
    def filter_vacancy(vacancy):
        organization = request.args.get('organization')
        if organization and organization not in vacancy.organization.name:
            return False

        position = request.args.get('position')
        if position and position not in vacancy.title:
            return False

        salary = request.args.get('salary')
        if salary and salary != str(vacancy.salary):
            return False

        return True

    res = session.query(Vacancy).filter_by(worker_id=None).all()
    return render_template("organization/job.html", vacancies=list(filter(filter_vacancy, res)), filters=request.args)
