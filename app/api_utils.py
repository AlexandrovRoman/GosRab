from flask_restful import abort


def get_or_abort(id_, cls):
    obj = cls.get_by(id=id_)
    if not obj:
        abort(404, message=f"{cls.__name__} with id {id_} not found")
    return obj