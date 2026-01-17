from datetime import datetime
from src.config import API_DATE_FORMAT, API_BASE_URL_CDI_MONTHLY, API_BASE_URL_CDI_YEARLY, API_BASE_URL_CDI_INTERESTS
import pandas as pd
import requests


class CdiFetchError(Exception):
    pass


def get_monthly_cdi_rate(date: datetime, end_date: datetime = None) -> float | list[dict[str, float]]:
    """Retorna uma, ou uma lista de taxas de CDI mensais para o período especificado."""
    data_inicial = date.strftime(API_DATE_FORMAT)
    data_final = end_date.strftime(API_DATE_FORMAT) if end_date else date.strftime(API_DATE_FORMAT)
    url = API_BASE_URL_CDI_MONTHLY
    params = {
        "formato": "json",
        "dataInicial": data_inicial,
        "dataFinal": data_final
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)

    if "erro" in df.columns:
        error = df["erro"]
        raise CdiFetchError(f"Dados de CDI não encontrados para a data {date.strftime('%Y-%m-%d')}: {error}")

    cdi_obj = df["valor"].astype(float)
    if len(cdi_obj) == 1:
        return cdi_obj.iloc[0] / 100  # A API retorna o CDI em percentual, converto para decimal por padrão
    else:
        cdi_list = []
        for idx, row in df.iterrows():
            cdi_list.append({row["data"]: float(row["valor"]) / 100})
        return cdi_list


def get_yearly_cdi_rate(date: datetime, end_date: datetime = None) -> float | list[dict[str, float]]:
    """Retorna uma, ou uma lista de taxas de CDI anualizadas para o período especificado."""
    data_inicial = date.strftime(API_DATE_FORMAT)
    data_final = end_date.strftime(API_DATE_FORMAT) if end_date else date.strftime(API_DATE_FORMAT)
    url = API_BASE_URL_CDI_YEARLY
    params = {
        "formato": "json",
        "dataInicial": data_inicial,
        "dataFinal": data_final
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)

    if "erro" in df.columns:
        error = df["erro"]
        raise CdiFetchError(f"Dados de CDI não encontrados para a data {date.strftime('%Y-%m-%d')}: {error}")

    cdi_obj = df["valor"].astype(float)
    if len(cdi_obj) == 1:
        return cdi_obj.iloc[0] / 100
    else:
        cdi_list = []
        for idx, row in df.iterrows():
            cdi_list.append({row["data"]: float(row["valor"]) / 100})
        return cdi_list


def get_cdi_interest_rates(date: datetime) -> float:
    """Retorna a taxa de juros CDI para uma data específica. Não utilizado atualmente."""
    url = API_BASE_URL_CDI_INTERESTS
    params = {
        "formato": "json",
        "dataInicial": date.strftime(API_DATE_FORMAT),
        "dataFinal": date.strftime(API_DATE_FORMAT)
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)

    if "erro" in df.columns:
        error = df["erro"]
        raise CdiFetchError(f"Dados de CDI não encontrados para a data {date.strftime('%Y-%m-%d')}: {error}")

    return df["valor"].astype(float).iloc[0]
