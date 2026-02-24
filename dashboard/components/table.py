from typing import Optional, List, Dict, Any
import pandas as pd
from dash import html, dash_table
from dashboard.components.ids import ComponentID


def render(
        table_id: ComponentID,
        dataframe: pd.DataFrame,
        page_size: int = 10,
        style_cell: Optional[Dict[str, Any]] = None,
        style_header: Optional[Dict[str, Any]] = None,
        style_data: Optional[Dict[str, Any]] = None,
        editable: bool = False,
        filter_action: str = "native",
        sort_action: str = "native",
        page_action: str = "native",
        class_name: str = "",
        columns: Optional[List[Dict[str, Any]]] = None
) -> html.Div:
    """
    Renderiza uma tabela interativa baseada em um DataFrame do Pandas.

    Args:
        table_id: Identificador único do componente
        dataframe: DataFrame a ser exibido
        page_size: Número de linhas por página
        style_cell: Estilos customizados para células
        style_header: Estilos customizados para cabeçalho
        style_data: Estilos customizados para dados
        editable: Se as células são editáveis
        filter_action: Tipo de filtro ("native", "custom", None)
        sort_action: Tipo de ordenação ("native", "custom", None)
        page_action: Tipo de paginação ("native", "custom", None)
        class_name: Classes CSS adicionais
        columns: Configuração customizada de colunas
    """
    default_style_cell = {
        'textAlign': 'left',
        'padding': '10px',
        'fontFamily': 'Arial, sans-serif'
    }

    default_style_header = {
        'backgroundColor': '#f8f9fa',
        'fontWeight': 'bold',
        'borderBottom': '2px solid #dee2e6'
    }

    default_style_data = {
        'backgroundColor': 'white',
        'borderBottom': '1px solid #dee2e6'
    }

    table = dash_table.DataTable(
        id=str(table_id),
        columns=columns or [{"name": col, "id": col} for col in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_size=page_size,
        style_cell={**default_style_cell, **(style_cell or {})},
        style_header={**default_style_header, **(style_header or {})},
        style_data={**default_style_data, **(style_data or {})},
        editable=editable,
        filter_action=filter_action,
        sort_action=sort_action,
        page_action=page_action,
        className=f"dash-table {class_name}".strip()
    )

    return html.Div(table, className="table-container")
