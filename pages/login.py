import json

from urllib.parse import parse_qs
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from utils.auther_service import AutherError
from utils.auth import AuthManager
from app import app
import templates.flash

label = "Вход"
is_hidden = True


def get_content() -> list:
    return [
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        dbc.Form(
                            [
                                html.Div(
                                    [
                                        dbc.Label("Имя пользователя", html_for="username"),
                                        dbc.Input(
                                            id="username",
                                            type="text",
                                        ),
                                        dbc.FormText(
                                            "Логин от учетной записи",
                                            color="secondary",
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    [
                                        dbc.Label("Пароль", html_for="password"),
                                        dbc.Input(
                                            id="password",
                                            type="password",
                                        ),
                                        dbc.FormText(
                                            "Пароль от учетной записи",
                                            color="secondary",
                                        ),
                                    ],
                                    className="mb-3",
                                ),
                                html.Div(
                                    dbc.Button(
                                        id="login",
                                        n_clicks=0,
                                        children="Войти",
                                    ),
                                    className="mb-3",
                                ),
                                html.Div(
                                    id="login_message",
                                    className="mb-3",
                                ),
                            ],
                        ),
                        width={"size": 4, "offset": 4},
                    )
                ),
            ]
        ),
    ]


@app.callback(
    Output(component_id="login_message", component_property="children"),
    Input("login", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    State("location", "search"),
    prevent_initial_call=True,
)
def set_cookie(_, username: str, password: str, q_s: str):
    parsed_query_string = parse_qs(q_s.lstrip("?"))
    try:
        token = AuthManager.get_token(username=username, password=password)
    except AutherError as error:
        return templates.flash.render(title=error.title, text=error.reason)
    if token:
        AuthManager.set_cookie(cookie=json.dumps({"token": token}))
        return dcc.Location(id="access_login", pathname="/", href=f"/{parsed_query_string.get('return-url', [''])[0]}")
