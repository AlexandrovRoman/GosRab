web: gunicorn manage:app
create_test_models: python utils/excel_DB.py
init: python flask db init
migrate: python flask db migrate
upgrade: python flask db upgrade
clear: python utils/clear_postgresql_db.py
shell: python flask shell