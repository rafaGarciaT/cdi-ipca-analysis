# src/storage/factory.py
from pathlib import Path
from typing import Callable
import pandas as pd
from src.storage.base import BaseStorage
from src.storage.excel_storage import ExcelStorage


class StorageFactory:

    @staticmethod
    def create_storage(
            storage_type: str,
            filepath: Path,
            schema_func: Callable[[], pd.DataFrame]
    ) -> BaseStorage:
        storage_map = {
            "excel": ExcelStorage,
        }

        storage_class = storage_map.get(storage_type.lower())
        if not storage_class:
            raise ValueError(f"Unknown storage type: {storage_type}")

        return storage_class(filepath, schema_func)
