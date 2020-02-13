from utils.urls import path
from .views import hello, cookie_test

urlpatterns = [
    path('hello/', hello, methods=['GET', 'POST']),
    path('start/', cookie_test),
]
