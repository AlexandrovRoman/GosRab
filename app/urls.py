from utils.urls import add_relative_path, include
from app import api
from app.BaseAPI import ApiEntryPoint

urlpatterns = [
    add_relative_path('/users/', include('users.urls')),
    add_relative_path('/', include('news.urls')),
    add_relative_path('/organization/', include('organization.urls'))
]

api.add_resource(ApiEntryPoint, '/login/<string:email>/<string:password>')
