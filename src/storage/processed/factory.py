from pathlib import Path
from typing import Callable
import pandas as pd
from src.storage.processed.base import BaseProcessedStorage
from src.storage.processed.excel_storage import ExcelProcessedStorage


class ProcessedStorageFactory:

    @staticmethod
    def create_storage(
            storage_type: str,
            filepath: Path,
            schema_func: Callable[[], pd.DataFrame]
    ) -> BaseProcessedStorage:
        storage_map = {
            "excel": ExcelProcessedStorage,
        }

        storage_class = storage_map.get(storage_type.lower())
        if not storage_class:
            raise ValueError(f"Tipo de persistência de dados processados desconhecido: {storage_type}")

        return storage_class(filepath, schema_func)
