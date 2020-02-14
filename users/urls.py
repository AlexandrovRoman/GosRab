from utils.urls import path
from .views import profile, cookie_test, login, logout

urlpatterns = [
    path('profile/', profile, methods=['GET', 'POST']),
    path('login/', login, methods=['GET', 'POST']),
    path('logout/', logout),
    path('start/', cookie_test),
]
