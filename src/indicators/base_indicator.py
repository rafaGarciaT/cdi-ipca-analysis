from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any


class BaseIndicator(ABC):
    def __init__(self, name: str, raw_storage, processed_storage):
        self.name = name
        self.raw_storage = raw_storage
        self.processed_storage = processed_storage

    @abstractmethod
    def fetch(self, start_dt: datetime, end_dt: datetime = None) -> Any:
        pass

    @abstractmethod
    def transform(self, raw_data: Any, dt: datetime) -> dict:
        pass

    def has_been_processed(self, dt: datetime) -> bool:
        try:
            self.raw_storage.load(dt.strftime("%Y-%m"))
            return True
        except FileNotFoundError:
            return False

    def save_raw(self, data: Any, dt: datetime):
        return self.raw_storage.save(data, dt.strftime("%Y-%m"))

    def load_processed(self, processed_data: dict):
        """Carrega dados processados."""
        self.processed_storage.register_data(processed_data)
