import templates.flash
from dash import dcc
import dash_bootstrap_components as dbc
from functools import wraps
from datetime import date
import plotly.graph_objects as go
import queries.dash.timelines
from app import app
from dash.dependencies import Input, Output, State, MATCH
import pandas as pd
import importlib
import datetime
import utils.dataframe
import utils
import base64
from utils.conditions import is_character_non_special


def graph_wrapper(tags=None, is_export_button_hidden=True):
    def wrap_func(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            graph = func(*args, **kwargs)
            match [len(graph.figure["data"]) == 0, is_export_button_hidden]:
                case [True, _]:
                    return templates.flash.render("", "По вашему запросу ничего не найдено")
                case [False, True]:
                    return add_events(graph, tags)
                case _:
                    unique_id = str(id(graph))
                    return [
                        add_events(graph, tags),
                        dbc.Button(
                            "Скачать",
                            id={"type": "download_button", "index": unique_id},
                            n_clicks=0,
                        ),
                        dcc.Download(id={"type": "download_export_xlsx", "index": unique_id}),
                        dcc.Store(
                            id={"type": "download_graph_store", "index": unique_id},
                            data=kwargs["data"].to_dict("records"),
                        ),
                        dcc.Store(
                            id={
                                "type": "download_label_store",
                                "index": unique_id,
                            },
                            data=importlib.import_module(func.__module__).label,
                        ),
                    ]

        return wrapper

    return wrap_func


def graph_wrapper_with_today_event(tags=None, is_export_button_hidden=True):
    def wrap_func(func):
        @graph_wrapper(tags, is_export_button_hidden)
        @wraps(func)
        def wrapper(*args, **kwargs):
            graph = func(*args, **kwargs)
            if isinstance(graph, dcc.Graph) and len(graph.figure["data"]) != 0:
                graph.figure = add_event(graph.figure, date.today(), find_max_values(graph), "Мы тут")
            return graph

        return wrapper

    return wrap_func


def add_event(fig: go.Figure, x: str, y: int, text: str) -> go.Figure:
    fig.add_shape(
        go.layout.Shape(
            type="line",
            x0=x,
            y0=0,
            x1=x,
            y1=y,
            line=go.layout.shape.Line(
                color="#333",
                width=1,
                dash="dot",
            ),
        )
    )
    fig.add_trace(
        go.Scatter(
            mode="markers",
            text=text,
            texttemplate="{}",
            hoverinfo=None,
            hoverlabel=None,
            hovertext=None,
            hovertemplate="",
            showlegend=False,
            name="",
            marker=go.scatter.Marker(
                symbol="diamond-tall",
                color="rgba(118,163,196,255)",
                size=20,
            ),
            x=[x],
            y=[0, y],
        )
    )
    return fig


def add_events(graph: dcc.Graph, tags: set) -> dcc.Graph:
    if tags and graph.figure["data"][0]["type"] == "scatter":
        events = queries.dash.timelines.events(
            tags=list(tags), start_date=min(graph.figure["data"][0]["x"]), end_date=max(graph.figure["data"][0]["x"])
        )
        for _, event in events.iterrows():
            graph.figure = add_event(graph.figure, event["created_date"], find_max_values(graph), event["event"])
    return graph


def find_max_values(graph: dcc.Graph, axis: str = "y") -> int:
    axis_max_value = []
    for line in graph.figure["data"]:
        axis_max_value.append(int(max(line[axis])))
    return max(axis_max_value)


@app.callback(
    Output({"type": "download_export_xlsx", "index": MATCH}, "data"),
    Input({"type": "download_button", "index": MATCH}, "n_clicks"),
    State({"type": "download_graph_store", "index": MATCH}, "data"),
    State({"type": "download_label_store", "index": MATCH}, "data"),
    prevent_initial_call=True,
)
def export_graph_to_xlsx(_, data: dict, label: str) -> dict:
    dataframe = pd.DataFrame(data)
    return {
        "filename": f"{label}_{datetime.date.today()}.xlsx",
        "content": base64.b64encode(
            utils.dataframe.convert_to_xlsx(
                dataframe,
                "".join(filter(is_character_non_special, label)),
            )
        ).decode(),
        "base64": True,
    }
