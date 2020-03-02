from utils.urls import path
from .views import organization, add_organization, organizations, menu_organization, job

# Add your urls
urlpatterns = [
    path('job/', job),
    path('profile/personnel/organization/', organization),
    path('profile/organizations/', organizations),
    path('profile/redact/add_organization/', add_organization),
    path('profile/menu_organization/', menu_organization),
]
