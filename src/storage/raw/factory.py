from pathlib import Path
from src.storage.raw.base import BaseRawStorage
from src.storage.raw.json_storage import JsonRawStorage


class RawStorageFactory:

    @staticmethod
    def create_storage(storage_type: str, data_type: str) -> BaseRawStorage:
        storage_map = {
            "json": JsonRawStorage,
        }

        storage_class = storage_map.get(storage_type.lower())
        if not storage_class:
            raise ValueError(f"Tipo de persistência de dados brutos desconhecido: {storage_type}")

        return storage_class(data_type)
