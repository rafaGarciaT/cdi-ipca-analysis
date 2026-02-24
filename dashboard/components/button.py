from dash import html
from dashboard.components.ids import ComponentID


def render(
    button_id: ComponentID,
    label: str = "",
    icon_class: str = "",
    variant: str = "primary",
    disabled: bool = False,
    size: str = "md",
    class_name: str = "",

) -> html.Button:
    """
    Cria um botão genérico.

    Args:
        button_id: ID único do botão
        label: Texto exibido no botão
        icon_class: Classe CSS do ícone (ex: 'fa fa-download')
        variant: Estilo do botão (primary, secondary, danger, success)
        disabled: Se o botão está desabilitado
        size: Tamanho do botão (sm, md, lg)
        class_name: Classes CSS adicionais

    Returns:
        Componente html.Button configurado
    """

    if not label and not icon_class:
        raise ValueError("Botão deve ter pelo menos um 'label' ou 'icon_class'")

    css_classes = f"btn btn-{variant} btn-{size} {class_name}".strip()

    children = []
    if icon_class:
        children.append(html.I(className=icon_class))
    if label:
        if icon_class:
            children.append(" ")
        children.append(label)

    return html.Button(
        children,
        id=str(button_id),
        disabled=disabled,
        className=css_classes,
        n_clicks=0)
