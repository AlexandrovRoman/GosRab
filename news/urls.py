from news.views import index
from utils.urls import relative_path

# Add your urls
urlpatterns = [
    relative_path('', index),
]
