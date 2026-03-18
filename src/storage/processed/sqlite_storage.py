from pathlib import Path
from typing import Callable

import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.storage.processed.sql_base_storage import BaseSQLProcessedStorage


class SQLiteProcessedStorage(BaseSQLProcessedStorage):
    """Implementação SQLite para armazenamento de dados processados."""

    def __init__(self, filepath: Path, schema_func: Callable[[], pd.DataFrame]) -> None:
        table_name = filepath.stem
        super().__init__(table_name, schema_func)
        self.filepath = filepath
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

        # Para garantir que a tabela exista desde o início
        self._ensure_table_exists()

    def _create_engine(self) -> Engine:
        db_path = self.filepath.resolve().as_posix()
        return create_engine(f"sqlite+pysqlite:///{db_path}")
