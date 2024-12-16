from dash import dcc, html
import dash_bootstrap_components as dbc
from natsort import humansorted
from utils.page import pages_menu_condition, pages_menu_condition_with_subcategories, by_label_sort_key, generate_link
from utils.category import categories_list_condition
import pages
import os
import base64

LOGO_IMAGE = base64.b64encode(open(os.path.join("static/logo.svg"), "rb").read()).decode()


def render(content):
    nav = [
        dbc.DropdownMenu(
            label=category.get_label(),
            children=create_menu(category),
            nav=True,
            align_end=True,
        )
        for category in pages.categories_provider.filter(lambda c: categories_list_condition(c)).sort_natural(
            by_label_sort_key
        )
    ]

    layout = html.Div(
        [
            html.Header(
                dbc.Navbar(
                    [
                        dbc.Container(
                            [
                                dcc.Link(
                                    html.Img(
                                        src=f"data:image/svg+xml;base64,{LOGO_IMAGE}",
                                        height="32px",
                                        className="logo",
                                    ),
                                    href="/",
                                ),
                                dbc.NavbarToggler(id="navbar-toggler"),
                                dbc.Collapse(
                                    dbc.Row(
                                        [
                                            html.Form(
                                                id="form",
                                                action="/",
                                                children=[
                                                    dcc.Input(
                                                        id="header-search-input",
                                                        type="search",
                                                        name="search",
                                                        placeholder="Искать отчёт",
                                                    ),
                                                    dbc.Button(
                                                        id="submit-button",
                                                        style={
                                                            "background": "#212121",
                                                            "border-radius": "0 4px 4px 0",
                                                            "min-width": "60px",
                                                            "z-index": "1",
                                                        },
                                                    ),
                                                ],
                                                style={"display": "flex"},
                                            ),
                                            dbc.Col(
                                                dbc.Nav(
                                                    nav,
                                                    className="mr-auto",
                                                    navbar=True,
                                                ),
                                                width="auto",
                                            ),
                                        ],
                                        className="ml-auto flex-nowrap mt-3 mt-md-0 w-100 justify-content-between",
                                        align="center",
                                    ),
                                    id="navbar-collapse",
                                    navbar=True,
                                ),
                            ],
                            className="container-layout",
                        )
                    ],
                    color="dark",
                    dark=True,
                    className="header-nav",
                ),
            ),
            html.Div(id="page-content", className="page-content container-layout container", children=content),
            html.Footer(
                [
                    html.Br(),
                    html.Br(),
                    html.Br(),
                ]
            ),
        ]
    )

    return layout


def generate_menu(category) -> list:
    return [
        dbc.DropdownMenuItem(**generate_link(page=page))
        for page in pages.pages_provider.filter(lambda p: pages_menu_condition(p, category.get_name())).sort_natural(
            by_label_sort_key
        )
    ]


def generate_menu_with_subcategory(category) -> list:
    items = []
    categories = humansorted(category.get_subcategories())
    for subcategory in categories:
        items.extend(
            [
                dbc.DropdownMenuItem(**generate_link(page=page))
                for page in pages.pages_provider.filter(
                    lambda p, subcategory=subcategory: pages_menu_condition_with_subcategories(
                        page=p, category_name=category.get_name(), subcategory_name=subcategory
                    )
                ).sort_natural(by_label_sort_key)
            ]
        )
        if categories[-1] != subcategory:
            items.append(dbc.DropdownMenuItem(divider=True))
    return items


def create_menu(category) -> list:
    if len(category.get_subcategories()) > 0:
        return generate_menu_with_subcategory(category)
    return generate_menu(category)
