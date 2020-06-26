from app import api
from .api import UserResource, UserApiEntryPoint
from .views import profile, logout, personnel, education, notification, t2, confirm_email
from .views import Login, EditProfile, Registration, ChangePassword, RestorePassword
from flask import Blueprint

bp = Blueprint("users", __name__, url_prefix="/users/")
bp.add_url_rule('profile/', view_func=profile)
bp.add_url_rule('profile/redact/', view_func=EditProfile.as_view("redact"), methods=['GET', 'POST'])
bp.add_url_rule('login/', view_func=Login.as_view("login"), methods=['GET', 'POST'])
bp.add_url_rule('logout/', view_func=logout)
bp.add_url_rule('profile/personnel/', view_func=personnel)
bp.add_url_rule('education/', view_func=education)
bp.add_url_rule('profile/notification/', view_func=notification)
bp.add_url_rule('registration/', view_func=Registration.as_view("registration"), methods=["GET", "POST"])
bp.add_url_rule('restore/', view_func=RestorePassword.as_view("restore"), methods=["GET", "POST"])
bp.add_url_rule('forgot/<email>/<token>/', view_func=ChangePassword.as_view("forgot"), methods=["GET", "POST"])
bp.add_url_rule('confirm/', view_func=confirm_email)
bp.add_url_rule('profile/t2/<int:user_id>', view_func=t2)

api.add_resource(UserApiEntryPoint, '/login/<string:email>/<string:password>', '/login', methods=["GET", "DELETE"])
api.add_resource(UserResource, '/user/<int:user_id>', '/user',  methods=['GET', 'DELETE', 'POST'])
