from dash import html


def render(code, text):
    return html.H1(code), html.P(text)
