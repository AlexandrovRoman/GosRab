from os import environ

# add your file containing models
models = [
    'users.models',
    'news.models',
    'organization.models',
]

# Special urlpatterns
urlpatterns = [
    'app.urls',
    'errors.views',
    'admin.urls',
]

HOST = environ.get('HOST', '127.0.0.1')
PORT = int(environ.get('PORT', 5000))
user = environ.get('DB_USERNAME', 'postgres')
url = environ.get('DB_URL', 'localhost:5432')
db = environ.get('DB_NAME', 'PFRProject')
password = environ.get('DB_PASSWORD', '')


class BaseConfig:
    WTF_CSRF_SECRET_KEY = environ.get('WTF_CSRF_SECRET_KEY', 'dsofpkoasodksap')
    SECRET_KEY = environ.get('SECRET_KEY', 'zxczxasdsad')
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{url}/{db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = environ.get('SECURITY_PASSWORD_SALT', 'iufsdivdjkvcbadb')
    EMAIL_SENDER_LOGIN = 'pfrproject2020@gmail.com'
    EMAIL_SENDER_PASSWORD = environ.get('EMAIL_SENDER_PASSWORD', '')


class ProductionConfig(BaseConfig):
    DEBUG = False
    CSRF_ENABLED = True


class DevelopConfig(BaseConfig):
    DEBUG = True
    ASSETS_DEBUG = True


Config = ProductionConfig
