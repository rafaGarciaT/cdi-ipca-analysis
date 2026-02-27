from dash import html, dcc
from dashboard.components.ids import ComponentID


def render(
        picker_id: ComponentID,
        label: str = "",
        initial_month: int = None,
        initial_year: int = None,
        display_format: str = 'MMMM YYYY',
        class_name: str = ""
) -> html.Div:
    children = []

    if label:
        children.append(html.Label(label, className="form-label"))

    children.append(
        dcc.DatePickerSingle(
            id=str(picker_id),
            display_format=display_format,
            initial_visible_month=f"{initial_year or 2020}-{initial_month or 1:02d}-01",
            className=class_name
        )
    )

    return html.Div(children, className="form-group")
