from typing import Any

import dash_bootstrap_components as dbc
from dash import html
from dash.html import Div


def render(title, text, color="warning"):
    return dbc.Alert(
        [
            html.H4(title, className="alert-heading"),
            html.P(text),
        ],
        color=color,
    )


def render_error_popover(title: str, text: Any, color: str = "danger") -> Div:
    return html.Div(
        [
            dbc.Button(
                title,
                id="hover-target",
                color=color,
                className="me-1",
                n_clicks=0,
            ),
            dbc.Popover(
                children=text,
                target="hover-target",
                body=True,
                trigger="hover",
                style={"overflow": "scroll", "maxHeight": "400px"},
            ),
        ]
    )
