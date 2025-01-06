from queries.main.users import get_last_actions
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import html, dash_table
import utils.table_format
import pandas as pd
from app import app

label = "Действия пользователя"

note = """
В отчете отображается список действия пользователя системы.
"""


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            id="get_last_actions",
                            n_clicks=0,
                            children="Показать",
                        ),
                        width=2,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="actions_users"),
    ]


@app.callback(
    Output(component_id="actions_users", component_property="children"),
    Input("get_last_actions", "n_clicks"),
    prevent_initial_call=True,
)
def update(
    _,
):
    data = get_last_actions()
    data["id"] = data.index + 1
    column_changes = {"username": "Логин", "action_time": "Время действия", "object_repr": "Что изменено"}
    data.rename(columns=column_changes, inplace=True)
    data["Время действия"] = pd.to_datetime(data["Время действия"]).dt.strftime("%d.%m.%Y %H:%M")
    return get_table(data[["id", "Логин", "Время действия", "Что изменено"]])


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
