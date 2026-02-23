from datetime import datetime
from src.config import API_BASE_URL_IPCA_MONTHLY
from src.fetch.base import fetch_bcb_data


class IpcaFetchError(Exception):
    """Exceção personalizada para erros de fetch de dados IPCA."""
    pass


def get_monthly_ipca(date: datetime, end_date: datetime = None) -> float | list[dict[str, float]]:
    """Retorna uma taxa, ou uma lista de taxas de IPCA mensais para o período especificado.

    Args:
        date (datetime): Data inicial (ou única) da consulta.
        end_date (datetime, optional): Data final da consulta. Se None, consulta apenas
            a data inicial. Defaults to None.

    Returns:
        float | list[dict[str, float]]: Se consulta de data única, retorna float com o valor.
            Se intervalo de datas, retorna lista de dicionários {data: valor}.
    """
    return fetch_bcb_data(API_BASE_URL_IPCA_MONTHLY, date, end_date, IpcaFetchError)
