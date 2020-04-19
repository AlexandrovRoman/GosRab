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
user = 'postgres'
url = 'localhost:5432'
db = 'PFRProject'
with open('postgresql_config.txt') as config:
    password = config.read().rstrip()


class BaseConfig:
    WTF_CSRF_SECRET_KEY = 'dsofpkoasodksap'
    SECRET_KEY = 'zxczxasdsad'
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{url}/{db}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECURITY_PASSWORD_SALT = 'iufsdivdjkvcbadb'
    EMAIL_SENDER_LOGIN = 'pfrproject2020@gmail.com'
    with open('top_secret.txt') as password_file:
        EMAIL_SENDER_PASSWORD = password_file.readline()


class ProductionConfig(BaseConfig):
    DEBUG = False
    CSRF_ENABLED = True


class DevelopConfig(BaseConfig):
    DEBUG = True
    ASSETS_DEBUG = True


Config = ProductionConfig
