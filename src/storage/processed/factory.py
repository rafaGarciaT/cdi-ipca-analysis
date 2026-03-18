from pathlib import Path
from typing import Callable
import pandas as pd
from src.storage.processed.base import BaseProcessedStorage
from src.storage.processed.csv_storage import CsvProcessedStorage
from src.storage.processed.excel_storage import ExcelProcessedStorage
from src.storage.processed.sqlite_storage import SQLiteProcessedStorage


class ProcessedStorageFactory:
    """Fábrica para criar instâncias de armazenamento de dados processados.
    Deve ser chamado pelo indicador com a string de tipo de armazenamento, o caminho do arquivo e a função de esquema correspondente.
    """

    @staticmethod
    def create_storage(storage_type: str, filepath: Path, schema_func: Callable[[], pd.DataFrame]) -> BaseProcessedStorage:
        """Cria uma instância de armazenamento de dados processados com base no tipo especificado, usando o caminho do arquivo e a função de esquema fornecidos para configurar a instância corretamente.

        Args:
            storage_type (str): Tipo de armazenamento a ser criado (por exemplo, "excel").
            filepath (Path): Caminho para o arquivo onde os dados processados serão armazenados.
            schema_func (Callable[[], pd.DataFrame]): Função de esquema referente ao indicador que chamou a fábrica.
        """
        storage_map = {
            "excel": ExcelProcessedStorage,
            "sqlite": SQLiteProcessedStorage,
            "csv": CsvProcessedStorage,
        }

        storage_class = storage_map.get(storage_type.lower())
        if not storage_class:
            raise ValueError(f"Tipo de persistência de dados processados desconhecido: {storage_type}")

        return storage_class(filepath, schema_func)
