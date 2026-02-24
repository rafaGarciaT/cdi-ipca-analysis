from dash import dcc, html
import plotly.graph_objects as go


def render_chart(figure: go.Figure, chart_id: str) -> html.Div:
    """Renderiza um gráfico Plotly genérico."""
    return html.Div(dcc.Graph(figure=figure),
        id=chart_id
    )