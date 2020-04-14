from app import session


class ModelMixin:
    def __init__(self, **db_columns):
        for col_name in db_columns:
            if not db_columns[col_name] is None:
                self.set_col(col_name, db_columns[col_name])

    def save(self):
        session.merge(self)
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
        obj.save()

    @classmethod
    def get_by(cls, **model_fields):
        return session.query(cls).filter_by(**model_fields).first()
