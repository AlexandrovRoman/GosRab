from utils.urls import path
from .views import hello, start

urlpatterns = [
    path('hello/', hello),
    path('start/', start),
]
