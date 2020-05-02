from utils.urls import relative_path
from app import api
from .api import OrganizationResource, OrganizationListResource
from .views import add_organization, organizations, menu_organization, job

# Add your urls
urlpatterns = [
    relative_path('job/', job),
    relative_path('profile/organizations/', organizations),
    relative_path('profile/redact/add_organization/', add_organization, methods=['GET', 'POST']),
    relative_path('profile/menu_organization/<int:org_id>/', menu_organization),
]

api.add_resource(OrganizationListResource, '/api/organization')
api.add_resource(OrganizationResource, '/api/organization/<string:api_token>/<int:org_id>')
