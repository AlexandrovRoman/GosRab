# add your file containing models
models = [
    'users.models',
    'news.models',
    'organization.models'
]

# Special urlpatterns
urlpatterns = [
    'app.urls',
    'errors.views',
    'admin.urls',
]

HOST = '127.0.0.1'
PORT = 5000


class BaseConfig:
    WTF_CSRF_SECRET_KEY = 'dsofpkoasodksap'
    SECRET_KEY = 'zxczxasdsad'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'my_precious_two'  # todo Поменять


class ProductionConfig(BaseConfig):
    DEBUG = False
    CSRF_ENABLED = True


class DevelopConfig(BaseConfig):
    DEBUG = True
    ASSETS_DEBUG = True


Config = ProductionConfig
