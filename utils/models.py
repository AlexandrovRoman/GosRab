from sqlalchemy_serializer import SerializerMixin
from app import db


class ModelMixin(SerializerMixin):
    ALL_LIMIT = 1000
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    def __init__(self, **db_columns):
        for col_name in db_columns:
            if not db_columns[col_name] is None and col_name in self.__dict__:
                setattr(self, col_name, db_columns[col_name])

    def save(self):
        db.session.merge(self) if self.id else db.session.add(self)
        db.session.commit()

    def delete(self):
        self.query.delete()
        db.session.commit()

    @classmethod
    def new(cls, *db_columns, **kdb_columns):
        """ Создание модели с автоматическим сохранением """

        obj = cls(*db_columns, **kdb_columns)
        obj.save()

    @classmethod
    def get_by(cls, **cols):
        return db.session.query(cls).filter_by(**cols).one()

    @classmethod
    def all(cls, offset=0, limits=False):
        res = cls.query
        if limits:
            res = res.limit(cls.ALL_LIMIT)
        if offset:
            res = res.offset(offset)
        return res
