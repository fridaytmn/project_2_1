import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output, State
from app import app
from utils.page import Page


def main_page(page: Page) -> dbc.Container:
    return dbc.Container(
        [
            html.H1(page.get_label(), className="title"),
            html.Div(page.get_content()),
        ]
    )


def report_page(page: Page) -> list:
    result = []
    result.append(
        html.Div(
            [
                dbc.Button(
                    "Сообщить о проблеме",
                    id="open_feedback_form",
                    n_clicks=0,
                ),
                html.Div(id="feedback_form"),
            ],
            className="button-report",
        ),
    )
    if page.get_note() is not None:
        result.append(
            html.Div(
                [
                    dbc.Button(
                        "Как работать с отчетом?",
                        id="open_button_id",
                        n_clicks=0,
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader(
                                "Как работать с отчетом",
                            ),
                            dbc.ModalBody(dcc.Markdown(page.get_note())),
                            dbc.ModalFooter(),
                        ],
                        id="note_modal_id",
                        is_open=False,
                        backdrop="static",
                        centered=True,
                    ),
                ],
                className="button-report",
            ),
        )
    result.append(html.H1(page.get_label(), className="title"))
    if not page.is_tags_hidden():
        result.append(
            html.Div(
                [
                    dcc.Link(
                        "#" + tag.value,
                        href="/?tag=" + tag.value,
                    )
                    for tag in page.get_tags()
                ],
                className="title-tags",
            )
        )
    result.append(html.Div(page.get_content()))
    return result


def render(page: Page):
    if page.get_short_path() == "index" or page.get_short_path() == "technical_work":
        return main_page(page)
    return report_page(page)


@app.callback(
    Output("note_modal_id", "is_open"),
    Input("open_button_id", "n_clicks"),
    [State("note_modal_id", "is_open")],
)
def toggle_note_collapse(open_click, is_open):
    if open_click:
        return not is_open
