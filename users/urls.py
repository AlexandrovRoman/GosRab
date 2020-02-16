from utils.urls import path
from .views import profile, cookie_test, login, logout, edit_profile, index

urlpatterns = [
    path('/', index, _main=True),
    path('profile/', profile),
    path('redact/', edit_profile, methods=['GET', 'POST']),
    path('login/', login, methods=['GET', 'POST']),
    path('logout/', logout),
    path('start/', cookie_test),
]
