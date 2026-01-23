from datetime import datetime
from src.config import API_BASE_URL_IPCA_MONTHLY
from src.fetch.base import fetch_bcb_data


class IpcaFetchError(Exception):
    pass


def get_monthly_ipca(date: datetime, end_date: datetime = None) -> float | list[dict[str, float]]:
    """Retorna uma, ou uma lista de taxas de IPCA mensais para o período especificado."""
    return fetch_bcb_data(API_BASE_URL_IPCA_MONTHLY, date, end_date, IpcaFetchError)
