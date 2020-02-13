from utils.urls import path
from .views import profile, cookie_test, education, job, community_work

urlpatterns = [
    path('profile/', profile, methods=['GET', 'POST']),
    path('education/', education, methods=['GET', 'POST']),
    path('job/', job, methods=['GET', 'POST']),
    path('community_work/', community_work, methods=['GET', 'POST']),
    path('start/', cookie_test),
]
