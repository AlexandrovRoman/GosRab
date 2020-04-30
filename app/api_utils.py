from flask_restful import abort


def abort_obj_not_found(id_, cls):
    obj = cls.get_by(id=id_)
    if not obj:
        abort(404, message=f"{cls.__name__} with id {id_} not found")
