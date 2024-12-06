from queries.main.users import get_count_users
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import html, dash_table
import utils.table_format
import pandas as pd
from app import app

label = "Список пользователей"

note = """
В отчете отображается список пользователей зарегистрированных в системе.
"""


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            id="get_count_users",
                            n_clicks=0,
                            children="Показать",
                        ),
                        width=2,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="count_users"),
    ]


@app.callback(
    Output(component_id="count_users", component_property="children"),
    Input("get_count_users", "n_clicks"),
    prevent_initial_call=True,
)
def update(
    _,
):
    data = get_count_users()
    data["id"] = data.index + 1
    column_changes = {"username": "Логин", "name": "ФИО"}
    data.rename(columns=column_changes, inplace=True)
    return get_table(data[["id", "Логин", "ФИО"]])


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="item_questions_table",
        columns=columns,
        style_cell_conditional=styles,
        page_size=50,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
    )
