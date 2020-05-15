from app import app, login_manager
from .views import forbidden, not_found_error, server_error, page_not_implemented, authorize

reg_er_hand = app.register_error_handler

urlpatterns = [
    reg_er_hand(403, forbidden),
    reg_er_hand(404, not_found_error),
    reg_er_hand(500, server_error),
    reg_er_hand(501, page_not_implemented),
    login_manager.unauthorized_handler(authorize),
]
