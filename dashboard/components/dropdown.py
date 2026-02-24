from dash import Dash, html, dcc

def render(
        app: Dash,
        title: str,
        contents: list,
        default_value: list | None = None,
        multi: bool = False
) -> html.Div:
    return html.Div(
        children=[
            html.H6(title),
            dcc.Dropdown(
                id="example-dropdown",
                options=[{"label": item, "value": item} for item in contents],
                value=default_value or contents,
                multi=multi
            ),
            html.Div(id="dropdown-output")
        ]
    )