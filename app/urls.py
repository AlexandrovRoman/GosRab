from utils.urls import add_relative_path, include
from app import api, app
from app.APIEntryPoints import UserApiEntryPoint, OrgApiEntryPoint
from news.urls import bp

app.register_blueprint(bp)
urlpatterns = [
    add_relative_path('/users/', include('users.urls')),
    add_relative_path('/organization/', include('organization.urls'))
]

api.add_resource(UserApiEntryPoint, '/login/<string:email>/<string:password>', '/login', methods=["GET", "DELETE"])
api.add_resource(OrgApiEntryPoint, '/org_login/<int:org_id>/<string:jwt>', '/org_login', methods=["GET", "DELETE"])
