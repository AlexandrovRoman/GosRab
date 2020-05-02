import datetime
from flask import render_template, request, redirect
from flask.views import MethodView, View
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
def menu_organization(org_id):
    org = Organization.get_by_id(current_user, org_id)
    if org is None:
        return 'Нет доступа'

    return render_template("organization/menu_organization.html", org=org)


@login_required
@check_confirmed
def personnel_department(org_id):
    org = Organization.get_by_id(current_user, org_id)
    if org is None:
        return 'Нет доступа'
    if request.method == 'POST':
        Vacancy(org_id=org_id, salary=request.form['salary'], title=request.form['title']).save()

    organization_info = {
        'org': org,
        'personnel': org.personnels,
        'workers': org.get_workers(),
        'required_workers': org.get_required_workers(),
    }

    return render_template("personnel_department.html", **organization_info, len=len)


class AddOrganization(MethodView):
    decorators = [login_required, check_confirmed]

    def get(self):
        form = AddOrganizationForm()
        return render_template("organization/add_organization.html", form=form)

    def post(self):
        form = AddOrganizationForm()
        if not form.validate_on_submit():
            return self.get()
        org = Organization(
                date=datetime.datetime.now().date(),
                name=form.name.data,
                org_type=form.org_type.data,
                org_desc=form.org_desc.data,
                owner_id=current_user.id
            )
        org.save(add=True)
        return redirect('/organization/profile/organizations/')


class Job(View):
    def filter_vacancy(self, vacancy):
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

    def dispatch_request(self):
        res = session.query(Vacancy).filter_by(worker_id=None).all()
        return render_template("organization/job.html", vacancies=list(filter(self.filter_vacancy, res)),
                               filters=request.args)
