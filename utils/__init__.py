import pandas as pd


def set_timezone(dataframe: pd.DataFrame) -> pd.DataFrame:
    datetime_with_tz = list(dataframe.select_dtypes(include=["datetime64[ns, UTC]"]).columns)
    datetime_without_tz = list(dataframe.select_dtypes(include=["<M8[ns]"]).columns)
    for column in datetime_with_tz:
        dataframe[column] = dataframe[column].dt.tz_convert(tz="Asia/Yekaterinburg")
    for column in datetime_without_tz:
        dataframe[column] = dataframe[column].dt.tz_localize(tz="Asia/Yekaterinburg")
    return dataframe
