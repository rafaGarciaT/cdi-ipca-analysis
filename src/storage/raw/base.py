from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseRawStorage(ABC):
    """Classe base para armazenamento de dados brutos."""

    @abstractmethod
    def save(self, data: Any, reference_date: str) -> str:
        """Salva os dados brutos usando a instância de armazenamento de dados brutos, organizando por mês e ano.

        Args:
            data (Any): Dados brutos a serem salvos.
            reference_date (str): Data associada aos dados no formato "YYYY-MM".

        Returns:
            str: Caminho ou identificador onde os dados brutos foram salvos.
        """
        pass

    @abstractmethod
    def load(self, date: str) -> dict:
        """Carrega os dados brutos para uma data específica, permitindo acesso aos dados organizados por mês e ano.

        Args:
            date (str): Data para a qual os dados brutos devem ser carregados, no formato "YYYY-MM".

        Returns:
            dict: Dicionário contendo os dados brutos carregados para a data especificada.
        """
        pass

    @abstractmethod
    def get_values_until(self, year: str, stop_date: str) -> list[float]:
        """Obtém os valores brutos para um ano específico até uma data de parada.

        Args:
            year (str): Ano para o qual os valores brutos devem ser obtidos, no formato "YYYY".
            stop_date (str): Data de parada para a obtenção dos valores brutos, no formato "YYYY-MM-DD".

        Returns:
            list[float]: Lista de valores brutos para o ano especificado até a data de parada.
        """
        pass

    @abstractmethod
    def get_collected_values(self, raw_dir: Path) -> set:
        """Obtém as datas para as quais os dados brutos já foram coletados. Feito para o Backfill.

        Args:
            raw_dir: Diretório onde os dados brutos estão armazenados.

        Returns:
            set: Conjunto de datas (no formato "YYYY-MM") para as quais os dados brutos já foram coletados.
        """
        pass
