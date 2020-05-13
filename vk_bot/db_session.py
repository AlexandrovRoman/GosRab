import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_uri, **params):
    global __factory

    if __factory:
        return

    if not db_uri or not db_uri.strip():
        raise Exception("Необходимо указать файл базы данных.")

    final_uri = f"{db_uri}?{'&'.join((f'{k}={v}' for k, v in params.items()))}" if params else db_uri

    print(f"Подключение к базе данных по адресу {final_uri}")

    engine = sa.create_engine(final_uri, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    import vk_bot.__all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    return __factory()
