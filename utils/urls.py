from app import app
from importlib import import_module
from warnings import warn

debug = app.debug


def add_url(url, func, methods):
    if not (isinstance(url, str) and hasattr(func, '__call__')):
        warn(f"Некорректные данные", Warning)
        return False
    app.add_url_rule(url, view_func=func, methods=methods)
    print(f'add url: {url}\n' if debug else '', end='')
    return True


def path(url: str, func, *, methods=['GET'], _main=False):
    if not hasattr(func, '__iter__'):
        if _main:
            return add_url(url, func, methods)
        else:
            return url, func, methods
    else:
        for url_, fnc, methods_ in func:
            if not add_url(url + url_, fnc, methods_):
                return False
        return True


def include(dir):
    try:
        pack = import_module(dir)
    except ModuleNotFoundError:
        raise ImportError(f"Не удалось найти {dir}.urlpatterns")
    try:
        patterns = getattr(pack, 'urlpatterns')
    except AttributeError:
        raise AttributeError(f'Файл {dir}.urlpatterns не содержит urlpatterns')
    print('include success\n' if debug else '', end='')
    for args in patterns:
        if isinstance(args, bool):
            continue
        yield args
