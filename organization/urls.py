from utils.urls import relative_path
from app import api
from .api import OrganizationResource, VacancyListResource
from .views import (organizations, menu_organization, send_resume, show_pretenders,
                    hire_worker, vacancies_organization, personnel_department)
from .views import AddOrganization, Job

# Add your urls
urlpatterns = [
    relative_path('job/', Job.as_view("job")),
    relative_path('profile/organizations/', organizations),
    relative_path('sendresume/<int:vacancy_id>', send_resume, methods=['GET', 'POST']),
    relative_path('profile/menu_organization/', menu_organization),
    relative_path('showpretenders/<int:vacancy_id>', show_pretenders, methods=['GET', 'POST']),
    relative_path('hireworker/<int:resume_id>', hire_worker, methods=['GET', 'POST']),
    relative_path('profile/redact/add_organization/',
                  AddOrganization.as_view("add_organization"), methods=['GET', 'POST']),
    relative_path('profile/menu_organization/<int:org_id>/', menu_organization),
    relative_path('menu/vacancies/<int:org_id>/', vacancies_organization),
    relative_path('menu/personnel_department/<int:org_id>/',
                  personnel_department, methods=['GET', 'POST']),
]

api.add_resource(VacancyListResource, '/vacancy')
api.add_resource(OrganizationResource, '/organization/<int:org_id>', '/organization/<int:org_id>/<string:org_token>',
                 '/organization',
                 methods=['GET', 'DELETE', 'POST'])
