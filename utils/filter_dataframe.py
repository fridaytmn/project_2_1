import pandas as pd
import re

OPERATORS = {
    "s>=": "ge",
    "sge": "ge",
    "sle": "le",
    "s<=": "le",
    "slt": "lt",
    "s<": "lt",
    "sgt": "gt",
    "s>": "gt",
    "sne": "ne",
    "s!=": "ne",
    "seq": "eq",
    "s=": "eq",
    "icontains": "contains",
    "scontains": "contains",
    "sdatestartswith": "datestartswith",
}


def filter_dataframe(filter_value: str, included_columns, dataframe: pd.DataFrame) -> pd.DataFrame:
    if filter_value is None or filter_value == "":
        return dataframe

    index_frame = dataframe.copy(deep=True).map(str)
    if included_columns:
        index_frame = index_frame[included_columns]

    return dataframe[index_frame.stack().str.contains(filter_value, case=False).groupby(level=0).any()]


def filter_dataframe_by_column(filter_query: str, dataframe: pd.DataFrame) -> pd.DataFrame:
    filtering_expressions = filter_query.split(" && ")
    for filter_part in filtering_expressions:
        try:
            dataframe = filter_column(filter_part, dataframe)
        except ValueError:
            return pd.DataFrame()
    return dataframe.reset_index(drop=True)


def filter_column(filter_part: str, dataframe: pd.DataFrame) -> pd.DataFrame:
    col_name, operator, filter_value = filter_query_parser(filter_part)
    if operator in ("eq", "ne", "lt", "le", "gt", "ge"):
        return use_comparison_operators(operator, dataframe, col_name, filter_value)
    if operator == "contains":
        return dataframe.loc[
            dataframe[col_name].astype(str).str.contains(re.escape(str(filter_value)), flags=re.IGNORECASE, regex=True)
        ]
    if operator == "datestartswith":
        return dataframe.loc[dataframe[col_name].str.startswith(filter_value)]
    return dataframe


def filter_query_parser(filter_part: str) -> tuple[str, str, str] | tuple[str, str, float]:
    """Парсит поисковый запрос по столбцу датафрейма.
    Parameters:
        filter_part: строка запроса
    Returns:
        Имя столбца по которому велся поиск, оператор поиска, подходящие значения.
    """
    get_column_name = re.compile(r"{(.*?)\}")  # noqa FS003
    column_name = get_column_name.match(filter_part).group(1)
    value = " ".join(filter_part.replace("{" + column_name + "}", "").split()[1:])
    real_operator = OPERATORS.get(filter_part.replace("{" + column_name + "}", "").split()[:1][0], None)
    if value[0] == value[-1] and value[0] in ("'", '"', "`"):
        return column_name, real_operator, value[1:-1].replace("\\" + value[0], value[0])
    try:
        match [value.find("."), value.find(",")]:
            case [-1, -1]:
                return column_name, real_operator, int(value)
            case [_, _]:
                return column_name, real_operator, float(value)
    except ValueError:
        return column_name, real_operator, value


def use_comparison_operators(operator: str, dataframe: pd.DataFrame, col_name: str, filter_value: str) -> pd.DataFrame:
    if filter_value is str and dataframe[col_name].dtype is not object:
        return dataframe
    try:
        return dataframe.loc[getattr(dataframe[col_name], operator)(filter_value)]
    except TypeError:
        return pd.DataFrame()
