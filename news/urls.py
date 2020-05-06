from news.views import index, news_info
from utils.urls import relative_path

# Add your urls
urlpatterns = [
    relative_path('', index),
    relative_path("news/<int:news_id>", news_info),
]
