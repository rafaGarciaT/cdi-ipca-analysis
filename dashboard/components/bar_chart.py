from dash import Dash, html, dcc
import plotly.express as px
from dash.dependencies import Input, Output

MEDAL_DATA = px.data.medals_long()

def render_medal(app: Dash, title: str) -> html.Div:
    @app.callback(
        Output("bar-chart", "children"),
        Input("example-dropdown", "value")
    )
    def update_bar_chart(selected_nations: list[str]) -> html.Div:
        filtered_data = MEDAL_DATA.query("nation in @selected_nations")

        if filtered_data.empty:
            return html.Div("No data available for the selected nations.", id="bar-chart")
        fig = px.bar(filtered_data, x="medal", y="count", color="nation", title=title)

        return html.Div(dcc.Graph(figure=fig), id="bar-chart")
    return html.Div(id="bar-chart")

