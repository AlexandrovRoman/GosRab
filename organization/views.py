import datetime
from flask import render_template, request, redirect, abort, url_for
from flask.views import MethodView, View
from flask_login import current_user, login_required
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
def send_resume(vacancy_id):
    vacancy = Vacancy.query.filter_by(id=vacancy_id).first_or_404()
    if vacancy.worker_id is not None:
        return 'Должность занята'
    form = SendResumeForm()
    if form.validate_on_submit():
        resume = Resume(
            user_id=current_user.id,
            vacancy_id=vacancy_id,
        )
        form.populate_obj(resume)
        resume.save(add=True)
        return redirect(url_for("organization.job"))

    return render_template("organization/send_resume.html", form=form)


@login_required
@check_confirmed
def menu_organization(org_id):
    org = Organization.get_by_id(current_user, org_id)
    if org is None:
        abort(403)

    return render_template("organization/menu_organization.html", org=org)


@login_required
@check_confirmed
def vacancies_organization(org_id):
    org = Organization.get_by_id(current_user, org_id)
    if org is None:
        abort(403)

    return render_template("organization/vacancies_organization.html", org=org)


@login_required
@check_confirmed
def personnel_department(org_id):
    org = Organization.get_by_id(current_user, org_id)
    if org is None:
        return abort(403)
    if request.method == 'POST':
        Vacancy(org_id=org_id, salary=request.form['salary'], title=request.form['title']).save(add=True)

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
    abort(403)


@login_required
@check_confirmed
def hire_worker(resume_id):
    resume = Resume.get_by(id=resume_id)
    if not resume:
        return abort(404)
    vacancy = resume.vacancy
    if vacancy.has_permission(current_user):
        for r in vacancy.resume:
            if r.id != resume_id:
                pass  # TODO: Выслать письма об отказе в пользу другого
            r.delete()
        vacancy.worker_id = resume.user_id
        vacancy.save()
        # TODO: Выслать письмо об принятии на должность
        return redirect(url_for('organization.organizations'))
    abort(403)

 
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
                owner_id=current_user.id
            )
        form.populate_obj(org)
        org.save(add=True)
        return redirect(url_for('organization.organizations'))


class Job(View):
    @staticmethod
    def filter_vacancy(vacancy):
        organization = request.args.get('organization')
        if organization and organization not in vacancy.organization.name:
            return False

        position = request.args.get('position')
        if position and position not in vacancy.content:
            return False

        salary = request.args.get('salary')
        if salary and salary != str(vacancy.salary):
            return False

        return True

    def dispatch_request(self):
        res = Vacancy.query.filter_by(worker_id=None).all()
        return render_template("organization/job.html", vacancies=list(filter(self.filter_vacancy, res)),
                               filters=request.args)
