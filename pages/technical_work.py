import dash_bootstrap_components as dbc
from dash import dcc


label = "Техническое обслуживание"


def get_content(params: dict):
    return dbc.Alert(
        dcc.Markdown(
            """
**Ведутся сервисные работы.**

Приносим извинения за неудобство.
""",
            style={"text-align": "center"},
        ),
        color="warning",
    )
