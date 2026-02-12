# src/storage/base.py
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
import pandas as pd


class BaseStorage(ABC):

    @abstractmethod
    def create_sheet(self, schema_func) -> pd.DataFrame:
        pass

    @abstractmethod
    def load_sheet(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def register_data(self, new_row: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_last_row(self, before_date: datetime) -> pd.Series | None:
        pass

    @abstractmethod
    def get_data(self, year: int | None = None, month: int | None = None, filepath: Path | None = None) -> pd.DataFrame:
        pass
