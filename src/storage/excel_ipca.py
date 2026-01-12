from datetime import datetime
from typing import Any
import pandas as pd
from pathlib import Path
from src.storage.schema import ipca_schema

current_directory = Path.cwd()
DATA_DIR = current_directory / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)


def create_ipca_sheet():
    df = ipca_schema()
    fpath = DATA_DIR / "ipca_data.xlsx"
    df.to_excel(fpath, index=False)
    return df


def load_ipca_sheet():
    fpath = DATA_DIR / "ipca_data.xlsx"
    return pd.read_excel(fpath)


def register_ipca_data(new_row: dict[str, Any]) -> None:
    fpath = DATA_DIR / "ipca_data.xlsx"

    if fpath.exists() is False:
        df = create_ipca_sheet()
    else:
        df = load_ipca_sheet()

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(fpath, index=False)


def get_last_ipca_row(before_date: datetime) -> pd.Series | None:
    fpath = DATA_DIR / "ipca_data.xlsx"

    if fpath.exists() is False:
        return None

    df = load_ipca_sheet()
    if df.empty:
        return None

    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"] < before_date]
    if df.empty:
        return None
    df = df.sort_values("date")

    return df.iloc[-1]

def get_last_ipca_accumulated(before_date: datetime) -> float:
    last = get_last_ipca_row(before_date)
    return float(last["ipca_accumulated"]) if last is not None else 0.0