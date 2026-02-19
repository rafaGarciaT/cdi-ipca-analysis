from abc import ABC, abstractmethod
from typing import Any


class BaseRawStorage(ABC):

    @abstractmethod
    def save(self, data: Any, reference_date: str) -> str:
        pass

    @abstractmethod
    def load(self, date: str) -> dict:
        pass

    @abstractmethod
    def get_values_until(self, year: str, stop_date: str) -> list[float]:
        pass

    @abstractmethod
    def get_collected_values(self, raw_dir)-> set:
        pass
