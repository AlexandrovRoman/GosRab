web: gunicorn manage:app
create_test_models: python utils/excel_DB.py
init: python manage.py db init
migrate: python manage.py db migrate
upgrade: python manage.py db upgrade
clear: python utils/clear_postgresql_db.py
shell: python manage.py shell