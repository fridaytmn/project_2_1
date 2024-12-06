from abc import ABC, abstractmethod
from typing import Any, NoReturn
import pandas as pd


class ConnectorInterface(ABC):
    @abstractmethod
    def execute_query(self, query: Any, *params, **kparams) -> pd.DataFrame:
        pass

    @abstractmethod
    def execute_command(self, command: Any, *params, **kparams) -> NoReturn:
        pass
