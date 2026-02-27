from enum import Enum
from dash import html, dcc
from dashboard.components.ids import ComponentID


class InputType(str, Enum):
    """Tipos válidos para campos de entrada HTML5."""
    TEXT = "text"
    PASSWORD = "password"
    EMAIL = "email"
    NUMBER = "number"
    SEARCH = "search"
    TEL = "tel"
    URL = "url"
    DATE = "date"
    TIME = "time"
    DATETIME_LOCAL = "datetime-local"


def render(
    input_id: ComponentID,
    label: str = "",
    placeholder: str = "",
    value: str = "",
    input_type: InputType = InputType.TEXT,
    disabled: bool = False,
    required: bool = False,
    class_name: str = "",
    debounce: bool = True
) -> html.Div:
    """
    Cria um campo de entrada genérico.

    Args:
        input_id: ID único do input
        label: Texto da etiqueta (opcional)
        placeholder: Texto de placeholder
        value: Valor inicial
        input_type: Tipo do input (text, password, email, number, search)
        disabled: Se o input está desabilitado
        required: Se o campo é obrigatório
        class_name: Classes CSS adicionais
        debounce: Se deve usar debounce nos callbacks (recomendado)

    Returns:
        Div contendo label (opcional) e input
    """
    children = []

    if label:
        children.append(
            html.Label(
                label + (" *" if required else ""),
                htmlFor=str(input_id),
                className="form-label"
            )
        )

    children.append(
        dcc.Input(
            id=str(input_id),
            type=input_type,
            placeholder=placeholder,
            value=value,
            disabled=disabled,
            required=required,
            className=f"form-control {class_name}".strip(),
            debounce=debounce
        )
    )

    return html.Div(children, className="form-group")

