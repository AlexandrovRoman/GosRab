from utils.urls import path
from .views import profile, cookie_test, login, logout, redact_profile

urlpatterns = [
    path('profile/', profile),
    path('redact/', redact_profile, methods=['GET', 'POST']),
    path('login/', login, methods=['GET', 'POST']),
    path('logout/', logout),
    path('start/', cookie_test),
]
