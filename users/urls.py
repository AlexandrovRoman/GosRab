from utils.urls import path
from .views import profile, cookie_test, login, logout, edit_profile, personnel, education, notification, job, organization, add_organization

urlpatterns = [
    path('profile/', profile),
    path('profile/redact/', edit_profile, methods=['GET', 'POST']),
    path('login/', login, methods=['GET', 'POST']),
    path('logout/', logout),
    path('start/', cookie_test),
    path('profile/personnel/', personnel),
    path('education/', education),
    path('profile/notification/', notification),
    path('job/', job),
    path('profile/personnel/organization', organization),
    path('profile/redact/add_organization', add_organization)
]
