from queries.main.users import get_active_staff
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import html, dash_table
import utils.table_format
import pandas as pd
from app import app

label = "Активные сотрудники"

note = """
В отчете отображается список активный сотрудников университета.
"""


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            id="get_active_staff",
                            n_clicks=0,
                            children="Показать",
                        ),
                        width=2,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="active_staff"),
    ]


@app.callback(
    Output(component_id="active_staff", component_property="children"),
    Input("get_active_staff", "n_clicks"),
    prevent_initial_call=True,
)
def update(
    _,
):
    data = get_active_staff()
    column_changes = {"username": "Логин", "email":"Почта", "date_joined": "Дата входа"}
    data["id"] = data.index + 1
    data.rename(columns=column_changes, inplace=True)
    data["Дата входа"] = pd.to_datetime(data["Дата входа"]).dt.strftime("%d.%m.%Y %H:%M")
    return get_table(data[["id", "Логин", "Почта", "Дата входа"]])

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
