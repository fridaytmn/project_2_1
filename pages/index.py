import dash_bootstrap_components as dbc
from dash import html, dcc
import pages
from utils.conditions import is_character_non_special
from utils.page import (
    SortType,
    pages_list_condition,
    by_label_sort_key,
)
from dash.dependencies import Input, Output
from app import app
from urllib.parse import parse_qs
from utils.category import categories_list_condition
from utils.page import pages_menu_condition, generate_link

is_hidden = True
label = "Отчеты"


def get_content(*args, **kwargs):
    return [
        dcc.Dropdown(
            id="index_sort_type",
            className="sort-type-wrapper",
            searchable=False,
            clearable=False,
            options=[
                {"label": "По популярности", "value": SortType.BY_HIT.value},
                {"label": "По алфавиту", "value": SortType.BY_NAME.value},
            ],
            value=SortType.BY_HIT.value,
            style={"border": "0px", "display": "none"},
        ),
        html.Div(id="index_reports_container", className="reports-wrapper"),
    ]


@app.callback(
    [
        Output("index_reports_container", "children"),
        Output("index_sort_type", "style"),
    ],
    Input("location", "search"),
    Input("index_sort_type", "value"),
)
def get_reports(
    query_string: str,
    sort_type_value: str,
):
    parsed_query_string = parse_qs(query_string.lstrip("?"))

    search_string = parsed_query_string.get("search", [None])[0]

    match sort_type_value:
        case SortType.BY_NAME.value:
            field_sorted_by = "label"
        case SortType.BY_HIT.value:
            field_sorted_by = None

    match search_string:
        case None:
            founded_ids = None
        case _:
            founded_ids = pages.search("".join(filter(is_character_non_special, search_string)), field_sorted_by)

    pages_sorted = pages.pages_provider.filter(lambda p: pages_list_condition(p, founded_ids))
    if query_string == "" or query_string == "?search=":
        return render_catalog(), {"border": "0px", "display": "none"}
    return render_search_result(pages_sorted=pages_sorted), {"border": "0px", "display": True}


def render_search_result(pages_sorted: list) -> list:
    return [
        dbc.Card(
            [
                dbc.ListGroupItem(**generate_link(page=page)),
                html.P(),
            ]
        )
        for page in pages_sorted
    ]


def render_catalog() -> list:
    return [
        dbc.Col(
            [
                dbc.Card(
                    [
                        dbc.CardHeader(
                            category.get_label(),
                        ),
                        dbc.ListGroup(
                            [
                                dbc.ListGroupItem(**generate_link(page=page))
                                for page in pages.pages_provider.filter(
                                    lambda p: pages_menu_condition(p, category.get_name())  # noqa: B023
                                ).sort_natural(by_label_sort_key)
                            ],
                            flush=True,
                        ),
                    ]
                )
                for category in pages.categories_provider.filter(lambda c: categories_list_condition(c)).sort_natural(
                    by_label_sort_key
                )
            ],
        )
    ]
