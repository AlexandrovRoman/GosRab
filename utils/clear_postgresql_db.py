from contextlib import closing
from pprint import pprint
from typing import Union
import psycopg2


class DB:
    def __init__(self, db_name: str, user: str, password: str, host: str, port: Union[int, str]):
        self.params = dict(dbname=db_name, user=user,
                           password=password, host=host, port=str(port))

    def get_tables(self):
        with closing(psycopg2.connect(**self.params)) as conn:
            with conn.cursor() as cursor:
                cursor.execute("""SELECT table_name FROM information_schema.tables
                                  WHERE table_schema NOT IN ('information_schema', 'pg_catalog')""")
                return [row[0] for row in cursor]

    def clear_tables(self):
        with closing(psycopg2.connect(**self.params)) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"DROP TABLE IF EXISTS {', '.join(self.get_tables())} CASCADE")
            conn.commit()


if __name__ == '__main__':
    from app import config
    db = DB(config.db, config.user, config.password, *config.url.split(":"))
    db.clear_tables()
    pprint(db.get_tables())
