from app import db


class ModelMixin:
    ALL_LIMIT = 1000

    def __init__(self, **db_columns):
        for col_name in db_columns:
            if not db_columns[col_name] is None:
                self.set_col(col_name, db_columns[col_name])

    def save(self, *, add=False):
        db.session.merge(self) if not add else db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def set_model(self, **db_columns):
        for col_name in db_columns:
            self.set_col(col_name, db_columns[col_name])

    def set_col(self, col_name, col_value):
        if col_name in self.__dict__:
            setattr(self, col_name, col_value)

    @classmethod
    def new(cls, *db_columns, **kdb_columns):
        obj = cls(*db_columns, **kdb_columns)
        obj.save(add=True)

    @classmethod
    def get_by(cls, **model_fields):
        return db.session.query(cls).filter_by(**model_fields).first()

    @classmethod
    def all(cls, offset=0, limits=False):
        res = db.session.query(cls)
        if limits:
            res = res.limit(cls.ALL_LIMIT)
        if offset:
            res = res.offset(offset)
        return res
