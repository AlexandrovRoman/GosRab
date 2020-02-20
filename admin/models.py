from flask import url_for, redirect
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class Roles:
    def is_accessible(self):
        roles_accepted = getattr(self, 'roles_accepted', None)
        return True if current_user.role in roles_accepted else False

    def _handle_view(self, *args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login', next="/admin"))
        if not self.is_accessible():
            return redirect(url_for('/'))


class AdminView(Roles, ModelView):
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
        return getattr(current_user, "role", None) in ['admin', 'superuser']

    def inaccessible_callback(self, name, **kwargs):
        return redirect('/')
