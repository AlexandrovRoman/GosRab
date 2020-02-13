import os

basedir = os.path.abspath(os.path.dirname(__file__))
# add your file containing models
models = [
    'users.models',
]


class Config:
    DEBUG = False
    CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'dsofpkoasodksap'
    SECRET_KEY = 'zxczxasdsad'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True
