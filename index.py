from typing import Union
import flask
from utils.WSGIServerClass import WebServer
from dash import html, ctx
from dash.dependencies import Input, Output
from app import app
import os
from utils.page import Page
import pages
import templates.main
import templates.layout
import templates.page
import templates.error
import utils
from utils.auth import AuthManager
from utils.user import User, ROLE

app.layout = templates.main.render(app)


def get_page(pathname: str, pages_provider: utils.page.PageProvider = pages.pages_provider) -> Page:
    """
    Функция убирает лишние слэши из пути, подменяет устаревшие ссылки на актуальные
    Отдает актуальную страницу пользователю
    """
    pathname = pathname.strip("/")
    if not pathname or pathname == "":
        pathname = "index"
    page = pages_provider.filter(lambda p: p.get_short_path() == pathname).one()
    if page is None or page.get_permanent_redirect() is None:
        return page
    return get_page(page.get_permanent_redirect(), pages_provider)


def render_page(page: Page, user: User) -> Union[html.Main, html.Div]:
    if AuthManager.authorize(user=user, page=page):
        return templates.layout.render(templates.page.render(page), user)
    if user.roles == {ROLE.GUEST}:
        return templates.layout.render(
            templates.error.render(
                401,
                [
                    html.Label("Требуется авторизация"),
                    html.A(" Вход", href=f"/login?return-url={page.get_short_path()}"),
                ],
            )
        )
    return templates.layout.render(
        templates.error.render(
            403,
            [
                html.Label("Недостаточно прав для просмотра отчета :("),
            ],
        )
    )


@app.callback(
    Output("base-content", "children"),
    Input("refresh-interval", "n_intervals"),
    Input("location", "pathname"),
    prevent_initial_call=True,
)
def display_page(_, pathname: str) -> (Union[html.Main, html.Div], bool):
    ctx.set_props(component_id="refresh-interval", props={"max_intervals": 0})
    page = get_page(pathname)
    match [bool(page), page.is_archived() if page else False, os.environ.get("TECHNICAL_WORK_ENABLE") == "1"]:
        case [_, _, True]:
            page = get_page("technical_work")
        case [False, _, False]:
            return templates.layout.render(templates.error.render(404, "Отчет не найден :("))
        case [True, True, False]:
            return templates.layout.render(templates.error.render(423, "Отчет перемещен в архив"))
    user = AuthManager.identify(cookie=flask.request.cookies.get("dash_cookie"))
    if not AuthManager.authenticate(user=user):
        user.roles = {ROLE.GUEST}
    return render_page(page, user)


def start_server() -> None:
    """
    Функция запускает сервер
    """
    mode = os.environ.get("MODE")
    app.server.logger.info(f"DASH IS STARTED IN {mode} MODE!")
    if mode == "PRODUCTION":
        httpd = WebServer(wsgi_app=app.server, listen="0.0.0.0", port=8050)
        httpd.serve_forever()
    else:
        app.run_server(debug=True, host="0.0.0.0", port=8051)


if __name__ == "__main__":
    start_server()
