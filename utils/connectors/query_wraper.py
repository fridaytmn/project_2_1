import functools
import pandas as pd
from utils.connectors import ConnectorInterface


def query(connector: ConnectorInterface, *params, **kparams):
    def wrap_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> pd.DataFrame:
            return connector.execute_query(func(*args, **kwargs), *params, **kparams)

        wrapper._original = func

        return wrapper

    return wrap_func
