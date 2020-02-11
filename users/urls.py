from utils.urls import path
from .views import hello

urlpatterns = [
    path('hello/', hello),
    path(),
]
