from utils.urls import relative_path
from .views import add_organization, organizations, menu_organization, job

# Add your urls
urlpatterns = [
    relative_path('job/', job),
    relative_path('profile/organizations/', organizations),
    relative_path('profile/redact/add_organization/', add_organization, methods=['GET', 'POST']),
    relative_path('profile/menu_organization/', menu_organization),
]
