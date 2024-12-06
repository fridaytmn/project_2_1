import functools
from typing import NoReturn
from utils.connectors import ConnectorInterface


def command(connector: ConnectorInterface):
    def wrap_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> NoReturn:
            connector.execute_command(func(*args, **kwargs))

        wrapper._original = func

        return wrapper

    return wrap_func
