from datetime import datetime
from pathlib import Path
from typing import Any
import pandas as pd
from src.storage.schema import cdi_schema
from src.config import pr_root

DATA_DIR = pr_root / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)
fpath = DATA_DIR / "cdi_data.xlsx"


def create_cdi_sheet() -> pd.DataFrame:
    """Cria a planilha Excel para armazenar os dados de CDI, caso ela não exista."""
    df = cdi_schema()
    df.to_excel(fpath, index=False)
    return df


def load_cdi_sheet() -> pd.DataFrame:
    """Carrega a planilha Excel que armazena os dados de CDI."""
    return pd.read_excel(fpath)


def register_cdi_data(new_row: dict[str, Any]) -> None:
    """Registra uma nova linha de dados de CDI na planilha Excel. Cria a planilha se ela não existir."""
    if not fpath.exists():
        df = create_cdi_sheet()
    else:
        df = load_cdi_sheet()

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(fpath, index=False)


def get_last_cdi_row(before_date: datetime) -> pd.Series | None:
    """Retorna a última linha de dados de CDI antes da data especificada."""
    if not fpath.exists():
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
    """Retorna o valor acumulado do CDI até a data especificada."""
    last = get_last_cdi_row(before_date)
    return float(last["cdi_accumulated"]) if last is not None else 0.0


def get_cdi_data(year: int | None = None, month: int | None = None, data_dir: Path | None = None) -> pd.DataFrame:
    """Devolve os dados de CDI filtrados por ano e mês, se fornecidos."""
    if data_dir is None:
        if not fpath.exists():
            return cdi_schema()
        df = load_cdi_sheet()
    else:
        local_fpath = Path(data_dir) / "cdi_data.xlsx"
        if not local_fpath.exists():
            return cdi_schema()
        df = pd.read_excel(local_fpath)

    date_dt = pd.to_datetime(df["date"], format="%Y-%m", errors="coerce")
    df = df.assign(_date_dt=date_dt)

    if year is not None:
        df = df[df["_date_dt"].dt.year == year]
    if month is not None:
        df = df[df["_date_dt"].dt.month == month]

    df = df.drop(columns=["_date_dt"])

    return df