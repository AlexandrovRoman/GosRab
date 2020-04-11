from app import session
from logging import error, basicConfig

basicConfig(format=u'%(levelname)-8s %(filename)s in [LINE:%(lineno)d]:\n%(message)s')


class ModelMixin:
    def __init__(self, **db_columns):
        for key in db_columns:
            if not db_columns[key] is None:
                setattr(self, key, db_columns[key])

    def save(self):
        try:
            session.add(self)
        except Exception as ex:
            error(f"{ex.__class__.__name__}: {ex}")
        finally:
            session.commit()

    @classmethod
    def new(cls, *db_columns, **kdb_columns):
        obj = cls(*db_columns, **kdb_columns)
        obj.save()

    @classmethod
    def get_by(cls, **model_fields):
        return session.query(cls).filter_by(**model_fields).first()
