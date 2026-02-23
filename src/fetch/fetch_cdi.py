from datetime import datetime
from src.config import API_BASE_URL_CDI_MONTHLY, API_BASE_URL_CDI_YEARLY, API_BASE_URL_CDI_INTERESTS
from src.fetch.base import fetch_bcb_data


class CdiFetchError(Exception):
    """Exceção personalizada para erros de fetch de dados CDI."""
    pass


def get_monthly_cdi_rate(date: datetime, end_date: datetime = None) -> float | list[dict[str, float]]:
    """Retorna uma taxa, ou uma lista de taxas de CDI mensais para o período especificado.

    Args:
        date (datetime): Data inicial (ou única) da consulta.
        end_date (datetime, optional): Data final da consulta. Se None, consulta apenas
            a data inicial. Defaults to None.

    Returns:
        float | list[dict[str, float]]: Se consulta de data única, retorna float com o valor.
            Se intervalo de datas, retorna lista de dicionários {data: valor}.
    """
    return fetch_bcb_data(API_BASE_URL_CDI_MONTHLY, date, end_date, CdiFetchError)


def get_yearly_cdi_rate(date: datetime, end_date: datetime = None) -> float | list[dict[str, float]]:
    """Retorna uma taxa, ou uma lista de taxas de CDI anualizadas para o período especificado.

    Args:
        date (datetime): Data inicial (ou única) da consulta.
        end_date (datetime, optional): Data final da consulta. Se None, consulta apenas
            a data inicial. Defaults to None.

    Returns:
        float | list[dict[str, float]]: Se consulta de data única, retorna float com o valor.
            Se intervalo de datas, retorna lista de dicionários {data: valor}.
    """
    return fetch_bcb_data(API_BASE_URL_CDI_YEARLY, date, end_date, CdiFetchError)


def get_cdi_interest_rates(date: datetime, end_date: datetime = None) -> float | list[dict[str, float]]:
    """Retorna uma taxa, ou uma lista de taxas de juros CDI para uma data específica. Não utilizado atualmente.

    Args:
        date (datetime): Data inicial (ou única) da consulta.
        end_date (datetime, optional): Data final da consulta. Se None, consulta apenas
            a data inicial. Defaults to None.

    Returns:
        float | list[dict[str, float]]: Se consulta de data única, retorna float com o valor.
            Se intervalo de datas, retorna lista de dicionários {data: valor}.
    """
    return fetch_bcb_data(API_BASE_URL_CDI_INTERESTS, date, end_date, CdiFetchError)
