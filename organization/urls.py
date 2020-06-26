from app import api
from .api import OrganizationResource, VacancyListResource, OrgApiEntryPoint
from .views import (organizations, menu_organization, send_resume, show_pretenders,
                    hire_worker, vacancies_organization, personnel_department)
from .views import AddOrganization, Job
from flask import Blueprint

bp = Blueprint("organization", __name__, url_prefix="/organization/")
bp.add_url_rule('job/', view_func=Job.as_view("job"))
bp.add_url_rule('profile/organizations/', view_func=organizations)
bp.add_url_rule('sendresume/<int:vacancy_id>', view_func=send_resume, methods=['GET', 'POST'])
bp.add_url_rule('profile/menu_organization/<int:org_id>/', view_func=menu_organization)
bp.add_url_rule('showpretenders/<int:vacancy_id>', view_func=show_pretenders, methods=['GET', 'POST'])
bp.add_url_rule('hireworker/<int:resume_id>', view_func=hire_worker, methods=['GET', 'POST'])
bp.add_url_rule('profile/redact/add_organization/',
                view_func=AddOrganization.as_view("add_organization"), methods=['GET', 'POST'])
bp.add_url_rule('menu/vacancies/<int:org_id>/', view_func=vacancies_organization)
bp.add_url_rule('menu/personnel_department/<int:org_id>/',
                view_func=personnel_department, methods=['GET', 'POST'])

api.add_resource(OrgApiEntryPoint, '/org_login/<int:org_id>/<string:jwt_>', '/org_login', methods=["GET", "DELETE"])
api.add_resource(VacancyListResource, '/vacancy')
api.add_resource(OrganizationResource, '/organization', methods=['GET', 'DELETE', 'POST'])
