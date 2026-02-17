from src.storage.processed.base import BaseProcessedStorage
from src.storage.processed.excel_storage import ExcelProcessedStorage
from src.storage.processed.factory import ProcessedStorageFactory
from src.storage.processed.schema import cdi_schema, ipca_schema

__all__ = [
    "BaseProcessedStorage",
    "ExcelProcessedStorage",
    "ProcessedStorageFactory",
    "cdi_schema",
    "ipca_schema",
]

__version__ = "0.2.0"
