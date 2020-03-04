from utils.urls import path
from .views import profile, cookie_test, login, logout, \
    edit_profile, personnel, education, notification, personnel_department, registration

urlpatterns = [
    path('profile/', profile),
    path('profile/redact/', edit_profile, methods=['GET', 'POST']),
    path('login/', login, methods=['GET', 'POST']),
    path('logout/', logout),
    path('start/', cookie_test),
    path('profile/personnel/', personnel),
    path('education/', education),
    path('profile/notification/', notification),
    path('profile/menu_organization/personnel_department/', personnel_department),
    path('registration/', registration)
]
