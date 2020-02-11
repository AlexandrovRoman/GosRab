import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'dsofpkoasodksap'
    SECRET_KEY = 'zxczxasdsad'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://webuser:web_password@localhost/webuser_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopConfig(Config):
    DEBUG = True
    ASSETS_DEBUG = True


def from_object(Config):
    return None