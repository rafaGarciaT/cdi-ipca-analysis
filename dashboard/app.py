from dash import Dash, html, dcc
from dash_bootstrap_components.themes import BOOTSTRAP
from dashboard.layouts.inflation_calculator import inflation_calculator_layout
from dashboard.layouts.nations_medal import nations_medal_layout


def main() -> None:
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "Inflação Através Do Tempo"
    app.layout = inflation_calculator_layout(app)
    app.run()

if __name__ == "__main__":
    main()