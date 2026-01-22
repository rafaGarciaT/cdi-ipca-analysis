from datetime import datetime
from typing import Any
import pandas as pd
from src.storage.schema import ipca_schema
from src.config import pr_root

DATA_DIR = pr_root / "data" / "processed"
DATA_DIR.mkdir(parents=True, exist_ok=True)
fpath = DATA_DIR / "ipca_data.xlsx"


def create_ipca_sheet() -> pd.DataFrame:
    """Cria a planilha Excel para armazenar os dados de IPCA, caso ela não exista."""
    df = ipca_schema()
    df.to_excel(fpath, index=False)
    return df


def load_ipca_sheet() -> pd.DataFrame:
    """Carrega a planilha Excel que armazena os dados de IPCA."""
    return pd.read_excel(fpath)


def register_ipca_data(new_row: dict[str, Any]) -> None:
    """Registra uma nova linha de dados de IPCA na planilha Excel. Cria a planilha se ela não existir."""
    if not fpath.exists():
        df = create_ipca_sheet()
    else:
        df = load_ipca_sheet()

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(fpath, index=False)


def get_last_ipca_row(before_date: datetime) -> pd.Series | None:
    """Retorna a última linha de dados de IPCA antes da data especificada."""
    if not fpath.exists():
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
    """Retorna o valor acumulado do IPCA até a data especificada."""
    last = get_last_ipca_row(before_date)
    return float(last["ipca_accumulated"]) if last is not None else 0.0


def get_ipca_data(year: int | None = None, month: int | None = None) -> pd.DataFrame:
    """Devolve os dados de CDI filtrados por ano e mês, se fornecidos."""
    if not fpath.exists():
        return ipca_schema()

    df = load_ipca_sheet()

    if year is not None:
        df = df[df["year"] == year]
    if month is not None:
        df = df[df["month"] == month]

    return df