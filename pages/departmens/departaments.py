from queries.main.departments import get_departments
from utils.table_wrapper import table_wrapper
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import html, dash_table
import utils.table_format
import pandas as pd
from app import app
import utils.user

label = "Список подразделений"

note = """
В отчете отображается список подразделений в компании.
"""

allowed_roles = {"ADMIN"}


def get_content() -> list:
    return [
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Button(
                            id="get_departments",
                            n_clicks=0,
                            children="Показать",
                        ),
                        width=2,
                    ),
                ],
            ),
            className="form-inline-wrapper",
        ),
        html.Div(id="departments"),
    ]


@app.callback(
    Output(component_id="departments", component_property="children"),
    Input("get_departments", "n_clicks"),
    prevent_initial_call=True,
)
def update(
    _,
):
    data = get_departments()
    data["id"] = data.index + 1
    column_changes = {"id": "id", "name": "Департамент"}
    data.rename(columns=column_changes, inplace=True)
    return get_table(data[["id", "Департамент"]])


@table_wrapper()
def get_table(data: pd.DataFrame) -> dash_table.DataTable:
    columns, styles = utils.table_format.generate(data)
    return dash_table.DataTable(
        id="departments_table",
        columns=columns,
        style_cell_conditional=styles,
        page_size=50,
        sort_action="custom",
        sort_by=[],
        data=data.to_dict("records"),
    )
