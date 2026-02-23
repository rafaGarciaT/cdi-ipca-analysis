from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from src.storage import BaseRawStorage, BaseProcessedStorage


class BaseIndicator(ABC):
    """Classe base para indicadores financeiros, definindo a estrutura e métodos comuns para fetch, transformação e armazenamento de dados.

    Attributes:
        name (str): Nome do indicador.
        raw_storage: Instância de armazenamento para dados brutos.
        processed_storage: Instância de armazenamento para dados processados.
    """
    def __init__(self, name: str, raw_storage: BaseRawStorage, processed_storage: BaseProcessedStorage) -> None:
        """Inicializa o indicador com nome e instâncias de armazenamento para dados brutos e processados.

        Args:
            name (str): Nome do indicador.
            raw_storage: Instância de armazenamento para dados brutos.
            processed_storage: Instância de armazenamento para dados processados.
        """
        self.name = name
        self.raw_storage = raw_storage
        self.processed_storage = processed_storage

    @abstractmethod
    def fetch(self, start_dt: datetime, end_dt: datetime = None) -> Any:
        """Busca os dados brutos para o período especificado. Deve ser implementado por cada indicador específico."""
        pass

    @abstractmethod
    def transform(self, raw_data: Any, dt: datetime) -> dict:
        """Transforma os dados brutos em um formato processado. Deve ser implementado por cada indicador específico."""
        pass

    def has_been_processed(self, dt: datetime) -> bool:
        """Verifica se os dados para a data especificada já foram processados, tentando carregar os dados brutos correspondentes.

        Args:
            dt (datetime): Data para a qual verificar se os dados já foram processados.

        Returns:
            bool: True se os dados já foram processados (ou seja, os dados brutos existem), False caso contrário.
        """
        try:
            self.raw_storage.load(dt.strftime("%Y-%m"))
            return True
        except FileNotFoundError:
            return False

    def save_raw(self, data: Any, dt: datetime) -> str:
        """Salva os dados brutos usando a instância de armazenamento de dados brutos, organizando por mês e ano.

        Args:
            data (Any): Dados brutos a serem salvos.
            dt (datetime): Data associada aos dados, usada para organizar o armazenamento por mês e ano.

        Returns:
            str: Caminho ou identificador do local onde os dados brutos foram salvos.
        """
        return self.raw_storage.save(data, dt.strftime("%Y-%m"))

    def load_processed(self, processed_data: dict) -> None:
        """Carrega dados processados usando a instância de armazenamento de dados processados.

        Args:
            processed_data (dict): Dados processados a serem carregados.
        """
        self.processed_storage.register_data(processed_data)
