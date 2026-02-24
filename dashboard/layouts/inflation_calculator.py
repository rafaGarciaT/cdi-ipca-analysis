from dash import Dash, html, dcc

def inflation_calculator_layout(app: Dash) -> html.Div:
    return html.Div(
        className="container",
        children=[
            html.H1("Inflation Calculator"),
            html.Div(
                children=[
                    html.Label("Initial Amount:"),
                    dcc.Input(id="initial-amount", type="number", value=1000),
                ]
            ),
            html.Div(
                children=[
                    html.Label("Start Year:"),
                    dcc.Input(id="start-year", type="number", value=2000),
                ]
            ),
            html.Div(
                children=[
                    html.Label("End Year:"),
                    dcc.Input(id="end-year", type="number", value=2020),
                ]
            ),
            html.Button("Calculate", id="calculate-button"),
            html.Div(id="result")
        ]
    )