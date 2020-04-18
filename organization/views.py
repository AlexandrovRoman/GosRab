from flask import render_template, request
from flask_login import current_user, login_required
from app import session
from organization.forms import AddOrganizationForm
from organization.models import Organization, Vacancy
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
        # Creation here
        pass

    return render_template("organization/add_organization.html", form=form)


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

    res = session.query(Vacancy).filter(Vacancy.worker_id is None).all()
    return render_template("organization/job.html", vacancies=list(filter(filter_vacancy, res)), filters=request.args)
