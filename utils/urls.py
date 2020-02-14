from app import app
from importlib import import_module
from warnings import warn


debug = app.debug

def path(url: str, func, *, methods=['GET'], _main=False):
    if not hasattr(func, '__iter__'):
        if _main:
            if not (isinstance(url, str) and hasattr(func, '__call__')):
                warn(f"Некорректные данные", Warning)
                return False
            app.add_url_rule(url, view_func=func, methods=methods)
            print(f'add url: {url}\n' if debug else '', end='')
            return True
        else:
            return url, func, methods
    else:
        for url_, fnc, methods_ in func:
            if not (isinstance(url_, str) and hasattr(fnc, '__call__')):
                warn(f"Некорректные данные", Warning)
                return False
            app.add_url_rule(url + url_, view_func=fnc, methods=methods_)
            print(f'add url: {url + url_}\n' if debug else '', end='')
        return True


def include(dir):
    try:
        pack = import_module(dir)
        try:
            patterns = getattr(pack, 'urlpatterns')
        except AttributeError:
            raise AttributeError(f'Файл {dir}.urlpatterns не содержит urlpatterns')
    except ModuleNotFoundError:
        raise ImportError(f"Не удалось найти {dir}.urlpatterns")
    print('include success\n' if debug else '', end='')
    for args in patterns:
        if isinstance(args, bool):
            continue
        yield args
