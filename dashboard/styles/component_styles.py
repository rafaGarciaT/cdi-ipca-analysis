"""Component-specific style configurations."""
from dashboard.components.ids import InputIDs, ButtonIDs

COMPONENT_STYLES = {
    str(InputIDs.INITIAL_AMOUNT): {
        "wrapper_class": "currency-input",
        "input_class": "form-control-lg"
    },
    str(InputIDs.START_YEAR): {
        "wrapper_class": "compact-input"
    },
    str(ButtonIDs.CALCULATE): {
        "button_style": {
            "padding": "10px 30px",
            "backgroundColor": "#007bff",
            "color": "white",
            "border": "none",
            "borderRadius": "5px",
            "cursor": "pointer",
            "marginTop": "20px"
        }
    }
}

COMMON_STYLES = {
    "input_row": {
        "display": "flex",
        "justifyContent": "space-around",
        "alignItems": "center",
        "marginBottom": "30px",
        "padding": "20px",
        "backgroundColor": "#f8f9fa",
        "borderRadius": "5px"
    },
    "label": {
        "fontWeight": "bold",
        "marginBottom": "5px"
    }
}


def get_style(component_id: str, key: str, default: str = "") -> str:
    """Get style for a specific component."""
    return COMPONENT_STYLES.get(component_id, {}).get(key, default)

def get_common_style(style_name: str) -> dict:
    """Get common reusable styles."""
    return COMMON_STYLES.get(style_name, {})