# TODO: This code not worked


from app.__init__ import app
from importlib import import_module
from warnings import warn


def path(url: str, func, *, _main=False):
    if not hasattr(func, '__iter__'):
        if _main:
            if not (isinstance(url, str) and hasattr(func, '__call__')):
                warn(f"Некорректные данные", Warning)
                return
            app.add_url_rule(url, view_func=func)
            print(f'add url: {url}')
        else:
            return url, func
    else:
        for url_, fnc in func:
            if not (isinstance(url_, str) and hasattr(fnc, '__call__')):
                warn(f"Некорректные данные", Warning)
                return
            app.add_url_rule(url + url_, view_func=fnc)
            print(f'add url: {url + url_}')


def include(dir):
    try:
        pack = import_module(dir)
        patterns = getattr(pack, 'urlpatterns')
    except ModuleNotFoundError:
        warn(f"Не удалось найти {dir}.urlpatterns", ImportWarning)
        return
    print('include success')
    yield from patterns
