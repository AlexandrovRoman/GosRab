from app import api
from utils.urls import relative_path
from .api import UserResource
from .views import profile, logout, personnel, education, notification, t2, confirm_email
from .views import Login, EditProfile, Registration, ChangePassword, RestorePassword

urlpatterns = [
    relative_path('profile/', profile),
    relative_path('profile/redact/', EditProfile.as_view("redact"), methods=['GET', 'POST']),
    relative_path('login/', Login.as_view("login"), methods=['GET', 'POST']),
    relative_path('logout/', logout),
    relative_path('profile/personnel/', personnel),
    relative_path('education/', education),
    relative_path('profile/notification/', notification),
    relative_path('registration/', Registration.as_view("registration"), methods=["GET", "POST"]),
    relative_path('restore/', RestorePassword.as_view("restore"), methods=["GET", "POST"]),
    relative_path('forgot/<email>/<token>/', ChangePassword.as_view("forgot"), methods=["GET", "POST"]),
    relative_path('confirm/', confirm_email),
    relative_path('profile/t2/<int:user_id>', t2)
]

api.add_resource(UserResource, '/user/<int:user_id>', '/user',  methods=['GET', 'DELETE', 'POST'])

