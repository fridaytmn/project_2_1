import dash_bootstrap_components as dbc
from dash.dependencies import ClientsideFunction
from dash import dcc, html
import os
import base64
from dash.dependencies import Input, Output, State

LOGO_IMAGE = base64.b64encode(open(os.path.join("static/logo.svg"), "rb").read()).decode()


def render(app):
    base_layout = html.Div(
        [
            dcc.Location(id="location"),
            html.Div(id="event_custom_error_view"),
            dbc.Toast(
                "",
                id="base-error",
                header="Ошибка",
                is_open=False,
                icon="danger",
                duration=5000,
                dismissable=True,
                style={
                    "position": "fixed",
                    "top": 81,
                    "zIndex": 100000,
                    "right": 10,
                    "width": 350,
                },
            ),
            dcc.Loading(
                id="content-loader",
                type="graph",
                fullscreen=True,
                children=html.Div(id="base-content"),
            ),
            dcc.Interval(
                id="refresh-interval",
                interval=5000,
                n_intervals=0,
            ),
        ]
    )

    @app.callback(
        Output("navbar-collapse", "is_open"),
        [Input("navbar-toggler", "n_clicks")],
        [State("navbar-collapse", "is_open")],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open

    app.clientside_callback(
        ClientsideFunction(
            namespace="clientside",
            function_name="show_feedback_form",
        ),
        Output("feedback_form", "data"),
        Input("open_feedback_form", "n_clicks"),
        prevent_initial_call=True,
    )

    return base_layout
