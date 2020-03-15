from organization.views import personnel_department
from utils.urls import relative_path
from .views import profile, cookie_test, login, logout, \
    edit_profile, personnel, education, notification, registration, t2

urlpatterns = [
    relative_path('profile/', profile),
    relative_path('profile/redact/', edit_profile, methods=['GET', 'POST']),
    relative_path('login/', login, methods=['GET', 'POST']),
    relative_path('logout/', logout),
    relative_path('start/', cookie_test),
    relative_path('profile/personnel/', personnel),
    relative_path('education/', education),
    relative_path('profile/notification/', notification),
    relative_path('profile/menu_organization/personnel_department/', personnel_department),
    relative_path('registration/', registration),
    relative_path('profile/t2/', t2)
]
