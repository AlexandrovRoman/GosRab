from app import session


class ModelMixin:
    def __init__(self, **db_columns):
        for col_name in db_columns:
            if not db_columns[col_name] is None:
                self.set_col(col_name, db_columns[col_name])

    def save(self, *, add=False):
        session.merge(self) if not add else session.add(self)
        session.commit()

    def delete(self):
        session.delete(self)
        session.commit()

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
        return session.query(cls).filter_by(**model_fields).first()

    @classmethod
    def all(cls, offset=0):
        return session.query(cls).filter(offset < cls.id < offset + 1000).all()
