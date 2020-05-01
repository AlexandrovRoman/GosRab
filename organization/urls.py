from utils.urls import relative_path
from app import api
from .api import OrganizationResource, OrganizationListResource
from .views import add_organization, organizations, menu_organization, job, send_resume, show_pretenders, hire_worker

# Add your urls
urlpatterns = [
    relative_path('job/', job),
    relative_path('profile/organizations/', organizations),
    relative_path('profile/redact/add_organization/', add_organization, methods=['GET', 'POST']),
    relative_path('/sendresume/<int:vacancy_id>', send_resume, methods=['GET', 'POST']),
    relative_path('profile/menu_organization/', menu_organization),
    relative_path('/showpretenders/<int:vacancy_id>', show_pretenders, methods=['GET', 'POST']),
    relative_path('/hireworker/<int:resume_id>', hire_worker, methods=['GET', 'POST']),
]

api.add_resource(OrganizationListResource, '/api/organization')
api.add_resource(OrganizationResource, '/api/organization/<string:api_token>/<int:org_id>')
