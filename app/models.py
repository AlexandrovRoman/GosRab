from app import session


def base_new(cls, special_commands=(), **kwargs):  # TODO: Сделать классом с возможностью наследования
    obj = cls()
    for key in kwargs:
        setattr(obj, key, kwargs[key])
    for command in special_commands:
        eval(command)
    session.add(obj)
    session.commit()
    return obj
