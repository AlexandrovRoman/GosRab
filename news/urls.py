from news.views import index
from utils.urls import path

# Add your urls
urlpatterns = [
    path('', index),
]
