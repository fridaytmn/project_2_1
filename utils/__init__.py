import pickle
import re
from dateutil.relativedelta import relativedelta
from apscheduler.schedulers.background import BackgroundScheduler
from dash import callback_context
import pandas as pd
import numpy as np
import os

_scheduler = None

allowed_users = [
    "vechk_aa",
    "pastukhov_k",
    "akhmirova_ap",
    "sosnin_as",
    "mikhaylov_ks",
    "udovenko_yua",
    "checherin_na",
    "smailova_da",
]
# список пользователей, которые всегда имеют доступ к категориям у которых есть get_allowed_groups


def get_scheduler():
    global _scheduler
    if _scheduler is None:
        _scheduler = BackgroundScheduler()
    return _scheduler


def escape(value):
    return re.sub(r"[^A-Za-z0-9а-яА-ЯёЁ\-]+", " ", value)


def calc_same_weekday(current, years=-1):
    """Calculates same weekday from current date.

    Often in sales reports and so on you need to compare this day to the same day last year,
    but based on the same "weekday", not "day of month".

    """
    result = current + relativedelta(
        day=current.day,
        month=current.month,
        year=current.year,
        years=years,
        weekday=current.weekday(),
    )
    return result


def pg_array(s) -> str:
    s = str(s)
    return "'" + s.replace("[", "{").replace("]", "}") + "'"


def get_is_triggered(input_id: str) -> bool:
    return input_id in [prop["prop_id"] for prop in callback_context.triggered][0]


def set_timezone(dataframe: pd.DataFrame) -> pd.DataFrame:
    datetime_with_tz = list(dataframe.select_dtypes(include=["datetime64[ns, UTC]"]).columns)
    datetime_without_tz = list(dataframe.select_dtypes(include=["<M8[ns]"]).columns)
    for column in datetime_with_tz:
        dataframe[column] = dataframe[column].dt.tz_convert(tz="Asia/Yekaterinburg")
    for column in datetime_without_tz:
        dataframe[column] = dataframe[column].dt.tz_localize(tz="Asia/Yekaterinburg")
    return dataframe


def to_pivot(dataframe: pd.DataFrame, shape: tuple) -> np.array:
    if dataframe.empty:
        return dataframe
    return np.vstack((np.reshape(pd.DataFrame(dataframe).columns.values, shape), pd.DataFrame(dataframe).to_numpy()))


def load_from_pickle_file(file_path: str, default: any = None) -> dict | list[str]:
    """Проверяет, существует ли необходимый pickle файл, и загружает его.
    Если файл отсутствует, то возвращает значение по умолчанию.
    Parameters:
        file_path: путь к файлу
        default: что вернуть, если файл отсутствует
    Return:
        содержимое файла или default
    """
    if os.path.exists(file_path):
        with open(file_path, "rb") as file:
            return pickle.load(file)
    return default
