from datetime import datetime
from typing import Any
import pandas as pd
from pathlib import Path
from src.storage.schema import cdi_schema

current_directory = Path.cwd()
DATA_DIR = current_directory / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def create_cdi_sheet():
    df = cdi_schema()
    fpath = DATA_DIR / "cdi_data.xlsx"
    df.to_excel(fpath, index=False)
    return df


def load_cdi_sheet():
    fpath = DATA_DIR / "cdi_data.xlsx"
    return pd.read_excel(fpath)


def register_cdi_data(new_row: dict[str, Any]) -> None:
    fpath = DATA_DIR / "cdi_data.xlsx"

    if fpath.exists() is False:
        df = create_cdi_sheet()
    else:
        df = load_cdi_sheet()

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(fpath, index=False)


def get_last_cdi_row(before_date: datetime) -> pd.Series | None:
    fpath = DATA_DIR / "cdi_data.xlsx"

    if fpath.exists() is False:
        return None

    df = load_cdi_sheet()
    if df.empty:
        return None

    df_year = df[df["year"] == before_date.year]
    if df_year.empty:
        return None
    df["month"] = pd.to_datetime(df["month"])
    df = df[df["month"] < before_date]
    if df.empty:
        return None
    df = df.sort_values("month")

    return df.iloc[-1]

def get_last_cdi_accumulated(before_date: datetime) -> float:
    last = get_last_cdi_row(before_date)
    return float(last["cdi_accumulated"]) if last is not None else 0.0