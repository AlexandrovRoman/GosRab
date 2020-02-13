from utils.urls import path
from .views import profile, cookie_test

urlpatterns = [
    path('profile/', profile, methods=['GET', 'POST']),
    path('start/', cookie_test),
]
