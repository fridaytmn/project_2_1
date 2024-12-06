from typing import NoReturn
import pandas as pd
import psycopg2
from utils.connectors import ConnectorInterface
from utils import set_timezone


class PostgreSQL(ConnectorInterface):
    def __init__(
        self,
        host: str = "localhost",
        user: str = "",
        password: str = "",
        database: str = "",
        application_name: str = "",
        port: int = 5432,
    ) -> NoReturn:
        self._host = host
        self._user = user
        self._port = port
        self._password = password
        self._database = database
        self._application_name = application_name

        self._connection = None

    def execute_query(self, query: str) -> pd.DataFrame:
        with self.create_connection() as connection:
            dataframe = pd.read_sql(query, connection)
        return set_timezone(dataframe)

    def execute_command(self, command: str) -> NoReturn:
        with self.create_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(command)
                connection.commit()

    def create_connection(self) -> NoReturn:
        return psycopg2.connect(
            host=self._host,
            user=self._user,
            port=self._port,
            password=self._password,
            database=self._database,
            application_name=self._application_name,
        )

    def __enter__(self) -> NoReturn:
        return self

    def __exit__(self) -> NoReturn:
        self._connection.close()
