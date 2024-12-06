from typing import Dict, List, Tuple
import pandas as pd
from dash.dash_table.Format import Format, Symbol
from utils.table_wrapper import THUMBNAIL_COLUMN_NAME
from dataclasses import dataclass
from urllib.parse import quote

BASE_URL = "https://www.sima-land.ru/search/?q="
MARKDOWN_COLUMN_REQUEST = "Запрос"
MARKDOWN_COLUMN_DETAILS = "Подробнее"


@dataclass
class TableColumn:
    name: str = ""
    type: str = ""
    suffix: str = ""
    group_delimiter: str = ","
    is_markdown: bool = False
    is_thumbnail: bool = False


group_type = {
    "float64": ",",
    "int16": ",",
    "int32": ",",
    "int64": ",",
    "uint8": ",",
    "uint16": ",",
    "uint32": ",",
    "uint64": ",",
    "datetime64[ns]": "",
    "datetime64[s]": "",
    "object": "",
    "bool": "",
    "datetime64[ns, UTC]": "",
    "datetime64[ns, Asia/Yekaterinburg]": "",
}

column_type = {
    "float64": "numeric",
    "int16": "numeric",
    "int32": "numeric",
    "int64": "numeric",
    "uint8": "numeric",
    "uint16": "numeric",
    "uint32": "numeric",
    "uint64": "numeric",
    "datetime64[ns]": "datetime",
    "datetime64[s]": "datetime",
    "object": "text",
    "bool": "any",
    "datetime64[ns, UTC]": "datetime",
    "datetime64[ns, Asia/Yekaterinburg]": "datetime",
}

column_text_align = {
    "float64": "right",
    "int16": "right",
    "int32": "right",
    "int64": "right",
    "uint8": "right",
    "uint16": "right",
    "uint32": "right",
    "uint64": "right",
    "datetime64[ns]": "right",
    "datetime64[s]": "right",
    "object": "left",
    "bool": "left",
    "datetime64[ns, UTC]": "right",
    "datetime64[ns, Asia/Yekaterinburg]": "right",
}


def generate(
    dataframe: pd.DataFrame,
    column_names: List = None,
    columns_with_suffix: List = None,
    columns_suffix: str = "",
    group_delimiter: str = ",",
) -> Tuple[List, List]:
    if column_names is None:
        column_names = dataframe.columns
    if columns_with_suffix is None:
        columns_with_suffix = []
    generate_url(dataframe)
    dtypes = dict(dataframe.dtypes)
    columns = [
        TableColumn(
            name=column_name,
            type=str(dtypes[column_name]) if column_name in dtypes else "object",
            suffix=columns_suffix if column_name in columns_with_suffix else "",
            group_delimiter=group_delimiter,
            is_markdown=column_name in {MARKDOWN_COLUMN_REQUEST, THUMBNAIL_COLUMN_NAME, MARKDOWN_COLUMN_DETAILS},
            is_thumbnail=column_name == THUMBNAIL_COLUMN_NAME,
        )
        for column_name in column_names
    ]

    return (
        generate_columns(columns),
        generate_columns_styles(columns),
    )


def generate_url(dataframe: pd.DataFrame):
    for column in dataframe:
        if column == MARKDOWN_COLUMN_REQUEST:
            dataframe[column] = dataframe[column].apply(lambda x: f"""[{str(x).strip()}]({BASE_URL + quote(str(x))})""")
    return dataframe


def generate_columns(columns: List[TableColumn]) -> List:
    return list(map(generate_column, columns))


def generate_columns_styles(columns: List[TableColumn]) -> List:
    return list(map(generate_column_style, columns))


def generate_column(column: TableColumn) -> Dict:
    return {
        "id": column.name,
        "name": column.name,
        "type": column_type[column.type],
        "format": Format(
            group=group_type[column.type],
            group_delimiter=column.group_delimiter,
            symbol=Symbol.yes,
            symbol_suffix=column.suffix,
        ),
        "presentation": "markdown" if column.is_markdown or column.is_thumbnail else "input",
    }


def generate_column_style(column: TableColumn) -> Dict:
    return {"if": {"column_id": column.name}, "textAlign": column_text_align[column.type]}


def generate_column_bars_style(dataframe: pd.DataFrame, column: str) -> List:
    n_bins = 100
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    ranges = [((dataframe[column].max() - dataframe[column].min()) * i) + dataframe[column].min() for i in bounds]
    styles = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        max_bound_percentage = bounds[i] * 100
        styles.append(
            {
                "if": {
                    "filter_query": (
                        f"{{{column}}} >= {min_bound}"
                        + (f" && {{{column}}} < {max_bound}" if (i < len(bounds) - 1) else "")
                    ),
                    "column_id": column,
                },
                "background": (
                    f"""
                    linear-gradient(90deg,
                    #3ec57f 0%,
                    #28b36b {max_bound_percentage}%,
                    #3a3a3b {max_bound_percentage}%,
                    #3a3a3b 100%)
                """
                ),
                "paddingBottom": 2,
                "paddingTop": 2,
            }
        )
    return styles


def generate_columns_bars_styles(dataframe: pd.DataFrame, columns_names: list) -> list:
    styles = []
    for column in columns_names:
        styles.extend(generate_column_bars_style(dataframe, column))
    return styles


def generate_row_highlighting_styles(columns: str, value: str, background_color: str = "#F5748E", color: str = "white"):
    styles = []
    for column in columns:
        styles.append(generate_row_highlighting_style(column, value, background_color, color))
    return styles


def generate_row_highlighting_style(column: str, value: str, background_color: str, color: str):
    return {
        "if": {"filter_query": f'{{{column}}} contains "{value}"'},
        "backgroundColor": background_color,
        "color": color,
    }


def generate_cell_highlighting_style(column: str, value: str, background_color: str, color: str):
    return {
        "if": {"filter_query": f'{{{column}}} contains "{value}"', "column_id": column},
        "backgroundColor": background_color,
        "color": color,
    }


def generate_row_fontweight_on_max_value_in_column(dataframe: pd.DataFrame, column: str, fontweight: str = "bold"):
    if column in dataframe.columns:
        return {
            "if": {"filter_query": f"{{{column}}} = {dataframe[column].max()}"},
            "fontWeight": fontweight,
        }


def generate_tooltip_data(data: pd.DataFrame, columns: list, note: str) -> list:
    """Добавляет всплывающую заметку к каждой ячейки из 'columns',
    текст заметки берется из колонки с названием 'note'"""
    tooltips_data = []
    for column in columns:
        for _, row in data.iterrows():
            tooltip_data = {column: {"value": f" Это {str(row[note])}", "type": "markdown"}}
            tooltips_data.append(tooltip_data)
    return tooltips_data
