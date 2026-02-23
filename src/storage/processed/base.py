from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any
import pandas as pd


class BaseProcessedStorage(ABC):
    """Classe base para armazenamento de dados processados."""

    @abstractmethod
    def create_sheet(self) -> pd.DataFrame:
        """Cria uma nova planilha (DataFrame) para armazenar os dados processados. Deve ser implementado por cada classe de armazenamento específica.

        Returns:
            pd.DataFrame: DataFrame vazio com as colunas apropriadas para armazenar os dados processados.
        """
        pass

    @abstractmethod
    def load_sheet(self) -> pd.DataFrame:
        """Carrega a planilha (DataFrame) existente com os dados processados. Deve ser implementado por cada classe de armazenamento específica.

        Returns:
            pd.DataFrame: DataFrame contendo os dados processados atualmente armazenados.
        """
        pass

    @abstractmethod
    def register_data(self, new_row: dict[str, Any]) -> None:
        """Registra uma nova linha de dados processados na planilha, garantindo que os dados sejam organizados por data e que a planilha seja atualizada corretamente. Deve ser implementado por cada classe de armazenamento específica.

        Args:
            new_row (dict[str, Any]): Dicionário contendo os dados a serem registrados.
        """
        pass

    @abstractmethod
    def get_last_row(self, before_date: datetime) -> pd.Series | None:
        """Obtém a última linha de dados processados antes de uma data específica, permitindo consultas históricas. Deve ser implementado por cada classe de armazenamento específica.

        Args:
            before_date (datetime): Data antes da qual a última linha de dados processados deve ser obtida.

        Returns:
            pd.Series | None: A última linha de dados processados como uma Series do pandas, ou None se não houver dados antes da data especificada.
        """
        pass

    @abstractmethod
    def get_data(self, year: int | None = None, month: int | None = None, filepath: Path | None = None) -> pd.DataFrame:
        """Obtém os dados processados para um período específico (ano e mês) ou a partir de um arquivo específico, permitindo flexibilidade na consulta dos dados. Deve ser implementado por cada classe de armazenamento específica.

        Args:
            year (int | None, optional): Ano para o qual os dados processados devem ser obtidos. Se None, não filtra por ano. Defaults to None.
            month (int | None, optional): Mês para o qual os dados processados devem ser obtidos. Se None, não filtra por mês. Defaults to None.
            filepath (Path | None, optional): Caminho para um arquivo específico de onde os dados processados devem ser obtidos. Se None, obtém os dados do armazenamento padrão. Defaults to None.

        Returns:
            pd.DataFrame: DataFrame contendo os dados processados para o período ou arquivo especificado
        """
        pass

    @abstractmethod
    def order_by_date(self, df: pd.DataFrame) -> pd.DataFrame:
        """Ordena um DataFrame de dados processados por data, garantindo que os dados estejam organizados cronologicamente. Deve ser implementado por cada classe de armazenamento específica.

        Args:
            df (pd.DataFrame): DataFrame contendo os dados processados a serem ordenados.

        Returns:
            pd.DataFrame: DataFrame ordenado por data.
        """
        pass
