from src.config import BCB_API_DATE_FORMAT
from src.indicators.base import BaseIndicator
from src.fetch import get_monthly_ipca
from src.storage import BaseRawStorage, BaseProcessedStorage
from src.transform.base_transform import calc_accumulated_ytd_rate
from datetime import datetime


class IPCAIndicator(BaseIndicator):
    """Indicador IPCA (Índice de Preços ao Consumidor Amplo).
    Coleta as taxas mensais do IPCA, calcula a taxa acumulada no ano e a taxa acumulada dos últimos 12 meses.

    Attributes:
        raw_storage: Armazenamento para dados brutos.
        processed_storage: Armazenamento para dados processados.
    """
    def __init__(self, raw_storage: BaseRawStorage, processed_storage: BaseProcessedStorage) -> None:
        """Inicializa o indicador IPCA com as instâncias de armazenamento para dados brutos e processados.

        Args:
            raw_storage: Instância de armazenamento para dados brutos.
            processed_storage: Instância de armazenamento para dados processados.
        """
        super().__init__("IPCA", raw_storage, processed_storage)

    def fetch(self, start_dt: datetime, end_dt: datetime = None) -> list:
        """Busca as taxas mensais e anualizadas do IPCA para o período especificado, retornando uma lista de tuplas (data, valor).

        Args:
            start_dt (datetime): Data inicial da consulta.
            end_dt (datetime, optional): Data final da consulta. Se None, consulta apenas a data inicial. Defaults to None.

        Returns:
            list: Lista de tuplas (data_str, monthly_rate), com os valores de taxas mensais do IPCA para cada data consultada.
        """
        data = get_monthly_ipca(start_dt, end_dt)
        # API pode retornar um único valor ou uma lista, normalizamos aqui
        if isinstance(data, list):
            result = []
            for entry in data:
                date_str = list(entry.keys())[0]
                result.append((date_str, entry[date_str]))
            return result
        else:
            date_str = start_dt.strftime(BCB_API_DATE_FORMAT)
            return [(date_str, data)]

    def transform(self, raw_data: float, dt: datetime) -> dict:
        """Transforma os dados brutos do IPCA em um formato processado, calculando as taxas acumuladas no ano e nos últimos 12 meses.
        Termina com um payload pronto para ser salvo no armazenamento de dados processados.

        Args:
            raw_data (float): Taxa mensal do IPCA.
            dt (datetime): Data associada aos dados, usada para calcular as taxas acumuladas.

        Returns:
            dict: Dicionário contendo todas as informações processadas.
        """
        monthly_rate = raw_data / 100

        monthly_rates_ytd = self.raw_storage.get_values_until(str(dt.year), dt.strftime("%Y-%m"))

        all_rates = monthly_rates_ytd
        if len(monthly_rates_ytd) < 12:
            prev_year_rates = self.raw_storage.get_values_until(str(dt.year - 1), f"{dt.year - 1}-12")
            all_rates = (prev_year_rates + monthly_rates_ytd)[-12:]

        last_12m = all_rates if len(all_rates) == 12 else None
        ytd_rate = calc_accumulated_ytd_rate(monthly_rates_ytd)
        rate_12m = calc_accumulated_ytd_rate(last_12m) if last_12m else float('nan')

        return {
            "date": dt.strftime("%Y-%m"),
            "ipca_monthly_rate": monthly_rate,
            "ipca_accumulated_ytd_rate": ytd_rate,
            "ipca_12m_rate": rate_12m
        }

    def save_raw(self, data: float, dt: datetime) -> None:
        """Salva os dados brutos do IPCA usando a instância de armazenamento de dados brutos, organizando por mês e ano.

        Args:
            data (float): Taxa mensal do IPCA.
            dt (datetime): Data associada aos dados, usada para organizar o armazenamento por mês e ano.
        """
        super().save_raw(round(data / 100, 6), dt)
