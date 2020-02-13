from utils.urls import path
from .views import index

urlpatterns = [
    path('', index)
]
