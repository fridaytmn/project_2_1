from functools import wraps
from dash.dependencies import Input, Output, State, MATCH
from dash import html, dcc
import dash_bootstrap_components as dbc

from app import app
import pandas as pd
import datetime
import importlib
import base64
import templates.flash
import utils
from utils.conditions import is_character_non_special
import utils.dataframe
from utils.filter_dataframe import filter_dataframe, filter_dataframe_by_column

THUMBNAIL_COLUMN_NAME = "Предпросмотр"
THUMBNAIL_HEIGHT = 130
THUMBNAIL_WIDTH = 164


def table_wrapper(columns=None):
    def wrap_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            table = func(*args, **kwargs)
            if len(table.data) == 0:
                return templates.flash.render("", "По вашему запросу ничего не найдено")
            unique_id = str(id(table))
            table.id = {"type": "table_search_table", "index": unique_id}

            return html.Div(
                [
                    dbc.DropdownMenu(
                        label="Скачать",
                        children=[
                            dbc.DropdownMenuItem(
                                "Без картинок XLSX",
                                id={"type": "table_export", "index": unique_id},
                                n_clicks=0,
                            ),
                            dbc.DropdownMenuItem(
                                "C картинками XLSX",
                                id={"type": "table_export_with_thumbnails", "index": unique_id},
                                n_clicks=0,
                                disabled=not next(
                                    (column for column in table.columns if column["name"] == "Предпросмотр"),
                                    False,
                                ),
                            ),
                        ],
                        color="secondary",
                    ),
                    dcc.Download(id={"type": "export_xlsx", "index": unique_id}),
                    dcc.Store(
                        id={"type": "table_search_store", "index": unique_id},
                        data=table.data,
                    ),
                    html.Div(
                        dcc.Input(
                            id={
                                "type": "table_search_input",
                                "index": unique_id,
                            },
                            type="text",
                            debounce=True,
                            placeholder="Поиск по таблице",
                        ),
                        className="header-table-search",
                    ),
                    dcc.Store(
                        id={
                            "type": "table_label_store",
                            "index": unique_id,
                        },
                        data=importlib.import_module(func.__module__).label,
                    ),
                    dcc.Store(
                        id={
                            "type": "table_search_included_columns_store",
                            "index": unique_id,
                        },
                        data=columns,
                    ),
                    html.Div(
                        table,
                        style={"overflow-x": "auto"},
                    ),
                ],
                className="table-wrapper",
            )

        return wrapper

    return wrap_func


@app.callback(
    Output({"type": "table_search_table", "index": MATCH}, "data"),
    Input({"type": "table_search_input", "index": MATCH}, "value"),
    Input({"type": "table_search_included_columns_store", "index": MATCH}, "data"),
    Input({"type": "table_search_table", "index": MATCH}, "sort_by"),
    Input({"type": "table_search_table", "index": MATCH}, "filter_query"),
    State({"type": "table_search_store", "index": MATCH}, "data"),
)
def table_actions(
    filter_value: str, included_columns: str, sort_by: list[dict], filter_query: str, data: list[dict]
) -> list[dict]:
    """
    Функция принимает данные и аргументы для их сортировки
    Так же фильтрует спец символы в filter_value
    """
    if filter_value is not None:
        filter_value = "".join(filter(is_character_non_special, filter_value))
    dataframe = pd.DataFrame(data)
    if not filter_query == "" and filter_query is not None:
        dataframe = filter_dataframe_by_column(filter_query, dataframe)
    return filter_dataframe(filter_value, included_columns, sort_dataframe(dataframe, sort_by)).to_dict("records")


@app.callback(
    Output({"type": "export_xlsx", "index": MATCH}, "data"),
    Input({"type": "table_export", "index": MATCH}, "n_clicks"),
    Input({"type": "table_export_with_thumbnails", "index": MATCH}, "n_clicks"),
    State({"type": "table_search_table", "index": MATCH}, "data"),
    State({"type": "table_label_store", "index": MATCH}, "data"),
    prevent_initial_call=True,
)
def export_table_to_xlsx(_, __, data: list, label: str) -> dict:
    is_thumbnails_enabled = utils.get_is_triggered("table_export_with_thumbnails")
    return {
        "filename": f"{label}_{datetime.date.today()}.xlsx",
        "content": base64.b64encode(
            utils.dataframe.convert_to_xlsx(
                [data],
                ["".join(filter(is_character_non_special, label))],
                THUMBNAIL_COLUMN_NAME,
                (THUMBNAIL_WIDTH, THUMBNAIL_HEIGHT),
                is_thumbnails_enabled,
            )
        ).decode(),
        "base64": True,
    }


def sort_dataframe(dataframe: pd.DataFrame, sort_by: list) -> pd.DataFrame:
    if len(sort_by) or not dataframe.empty:
        dataframe.sort_values(
            [col["column_id"] for col in sort_by],
            ascending=[col["direction"] == "asc" for col in sort_by],
            inplace=True,
        )
    return dataframe
