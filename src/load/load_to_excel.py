import pandas as pd
from pathlib import Path
from typing import Any, TypeAlias, List

current_directory = Path.cwd()
DATA_DIR = current_directory.parent.parent / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def create_cdi_sheet():
    df = pd.DataFrame({
        "date": [],
        "cdi_daily": [],
        "cdi_annual": [],
    })
    fpath = DATA_DIR / "cdi_data.xlsx"
    df.to_excel(fpath, index=False)
    return df


def create_ipca_sheet():
    df = pd.DataFrame({
        "date": [],
        "ipca_monthly": [],
        "ipca_annual": [],
    })
    fpath = DATA_DIR / "ipca_data.xlsx"
    df.to_excel(fpath, index=False)
    return df


def load_cdi_sheet():
    fpath = DATA_DIR / "cdi_data.xlsx"
    return pd.read_excel(fpath)


def load_ipca_sheet():
    fpath = DATA_DIR / "ipca_data.xlsx"
    return pd.read_excel(fpath)


def register_cdi_data(new_row: dict[str, Any]) -> None:
    fpath = DATA_DIR / "cdi_data.xlsx"

    if fpath.exists() is False:
        df = create_cdi_sheet()
    else:
        df = load_cdi_sheet()

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(fpath, index=False)


def register_ipca_data(new_row: dict[str, Any]) -> None:
    fpath = DATA_DIR / "ipca_data.xlsx"

    if fpath.exists() is False:
        df = create_ipca_sheet()
    else:
        df = load_ipca_sheet()

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(fpath, index=False)

