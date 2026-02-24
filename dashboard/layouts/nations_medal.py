from dash import Dash, html

from dashboard.components.bar_chart import render_medal as render_bar_chart
from dashboard.components.dropdown import render as render_dropdown

def nations_medal_layout(app: Dash) -> html.Div:
    return html.Div(
        className="container",
        children=[

            html.H1("Medalhas por Nação"),
            render_dropdown(app, "Selecione as Nações", ["South Korea", "China", "Canada"], multi=True),
            render_bar_chart(app, "Medalhas por Nação")

        ]
    )