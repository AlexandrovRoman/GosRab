from utils.urls import add_relative_path, include

urlpatterns = [
    add_relative_path('/users/', include('users.urls')),
    add_relative_path('/', include('news.urls')),
    add_relative_path('/organization/', include('organization.urls'))
]
