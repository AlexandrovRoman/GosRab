from sqlalchemy_utils import database_exists, create_database, drop_database


def resetdb_command(db_uri):
    """Destroys and creates the database."""
    if database_exists(db_uri):
        print('Deleting database.')
        drop_database(db_uri)
    if not database_exists(db_uri):
        print('Creating database.')
        create_database(db_uri)


if __name__ == '__main__':
    from app import app
    resetdb_command(app.config['SQLALCHEMY_DATABASE_URI'])
