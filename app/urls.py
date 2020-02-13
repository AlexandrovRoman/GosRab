from utils.urls import path, include

urlpatterns = [
    path('/users/', include('users.urls')),
    path('/', include('users.index_urls'))
]
