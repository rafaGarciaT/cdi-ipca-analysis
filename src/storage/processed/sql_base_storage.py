from abc import abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import Engine

from src.storage.processed.base import BaseProcessedStorage


class BaseSQLProcessedStorage(BaseProcessedStorage):
    """Classe base para armazenamento de dados processados em bancos SQL.
    Subclasses precisam apenas implementar _create_engine()."""

    def __init__(self, table_name: str, schema_func: Callable[[], pd.DataFrame]) -> None:
        self.table_name = table_name
        self.schema_func = schema_func
        self._engine: Engine | None = None

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            self._engine = self._create_engine()
        return self._engine

    @abstractmethod
    def _create_engine(self) -> Engine:
        """Cria e retorna um engine SQLAlchemy. Implementado por cada backend SQL."""
        pass

    def _ensure_table_exists(self) -> None:
        inspector = inspect(self.engine)
        if self.table_name not in inspector.get_table_names():
            self.create_sheet()

    def create_sheet(self) -> pd.DataFrame:
        schema = self.schema_func()
        schema.to_sql(self.table_name, self.engine, if_exists="replace", index=False)
        return schema

    def load_sheet(self) -> pd.DataFrame:
        self._ensure_table_exists()
        return pd.read_sql_table(self.table_name, self.engine)

    def register_data(self, new_row: dict[str, Any]) -> None:
        self._ensure_table_exists()
        df_row = pd.DataFrame([new_row])
        df_row.to_sql(self.table_name, self.engine, if_exists="append", index=False)

    def get_last_row(self, before_date: datetime) -> pd.Series | None:
        df = self.load_sheet()
        if df.empty:
            return None

        df["date"] = pd.to_datetime(df["date"])
        df = df[df["date"] < before_date]
        if df.empty:
            return None

        return df.sort_values("date").iloc[-1]

    def get_data(self, year: int | None = None, month: int | None = None, filepath: Path | None = None) -> pd.DataFrame:
        df = self.load_sheet()
        if df.empty:
            return df

        df["date"] = pd.to_datetime(df["date"])

        if year is not None:
            df = df[df["date"].dt.year == year]
        if month is not None:
            df = df[df["date"].dt.month == month]

        return df

    def order_by_date(self, df: pd.DataFrame) -> pd.DataFrame:
        df["date"] = pd.to_datetime(df["date"])
        return df.sort_values("date")
