"""CSS file loader for dashboard stylesheets."""
from pathlib import Path

STYLES_DIR = Path(__file__).parent / "assets" / "css"

def get_external_stylesheets() -> list[str]:
    """Returns list of external CSS files to load."""
    return [
        "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css",
    ]

def get_dashboard_stylesheet(dashboard_name: str) -> str:
    """Get path to dashboard-specific CSS file."""
    css_file = STYLES_DIR / f"{dashboard_name}.css"
    if css_file.exists():
        return f"/assets/css/{dashboard_name}.css"
    return ""

def get_common_stylesheet() -> str:
    """Get path to common CSS file."""
    return "/assets/css/common.css"
