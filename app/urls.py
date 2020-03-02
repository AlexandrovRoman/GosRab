from utils.urls import path, include

urlpatterns = [
    path('/users/', include('users.urls')),
    path('/', include('news.urls')),
    path('/organization/', include('organization.urls'))
]
