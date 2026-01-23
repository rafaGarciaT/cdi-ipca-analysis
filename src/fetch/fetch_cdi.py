from datetime import datetime
from src.config import API_BASE_URL_CDI_MONTHLY, API_BASE_URL_CDI_YEARLY, API_BASE_URL_CDI_INTERESTS
from src.fetch.base import fetch_bcb_data


class CdiFetchError(Exception):
    pass


def get_monthly_cdi_rate(date: datetime, end_date: datetime = None) -> float | list[dict[str, float]]:
    """Retorna uma, ou uma lista de taxas de CDI mensais para o período especificado."""
    return fetch_bcb_data(API_BASE_URL_CDI_MONTHLY, date, end_date, CdiFetchError)


def get_yearly_cdi_rate(date: datetime, end_date: datetime = None) -> float | list[dict[str, float]]:
    """Retorna uma, ou uma lista de taxas de CDI anualizadas para o período especificado."""
    return fetch_bcb_data(API_BASE_URL_CDI_YEARLY, date, end_date, CdiFetchError)


def get_cdi_interest_rates(date: datetime, end_date: datetime = None) -> float:
    """Retorna a taxa de juros CDI para uma data específica. Não utilizado atualmente."""
    return fetch_bcb_data(API_BASE_URL_CDI_INTERESTS, date, end_date, CdiFetchError)
