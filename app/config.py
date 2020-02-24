import os

basedir = os.path.abspath(os.path.dirname(__file__))
# add your file containing models
models = [
    'users.models',
    'news.models',
    'organisations.models'
]
# Special urlpatterns
urlpatterns = [
    'app.urls',
    'errors.views',
    'admin.urls',
]


class BaseConfig:
    WTF_CSRF_SECRET_KEY = 'dsofpkoasodksap'
    SECRET_KEY = 'zxczxasdsad'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(BaseConfig):
    DEBUG = False
    CSRF_ENABLED = True


class DevelopConfig(BaseConfig):
    DEBUG = True
    ASSETS_DEBUG = True


Config = ProductionConfig
