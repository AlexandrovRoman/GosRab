from flask import url_for, redirect
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class Roled:
    def is_accessible(self):
        roles_accepted = getattr(self, 'roles_accepted', None)
        for role in current_user.roles:
            print(role.role_name, roles_accepted)
            if role.role_name in roles_accepted:
                return True

    def _handle_view(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next="/admin"))
        if not self.is_accessible():
            return redirect(url_for('/'))


class AdminView(Roled, ModelView):
    def __init__(self, *args, **kwargs):
        self.roles_accepted = kwargs.pop('roles_accepted', list())
        super().__init__(*args, **kwargs)


class NewsView(AdminView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class StatisticView(AdminView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HomeAdminView(AdminIndexView):
    def is_accessible(self):
        for role in getattr(current_user, "roles", None):
            if role.role_name in ['admin', 'superuser']:
                return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/')
