from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import requests

class CdiFetchError(Exception):
    pass

def get_cdi(date: datetime) -> float:
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados"
    params = {
        "formato": "json",
        "dataInicial": date.strftime("%d/%m/%Y"),
        "dataFinal": date.strftime("%d/%m/%Y")
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)

    if "erro" in df.columns:
        error = df["erro"]
        raise CdiFetchError(f"Dados de CDI não encontrados para a data {date.strftime('%Y-%m-%d')}: {error}")

    return df["valor"].astype(float).iloc[0]


def get_monthly_cdi_rate(date: datetime, end_date: datetime=None) -> float | list[dict[str, float]]:
    data_inicial = date.strftime("%d/%m/%Y")
    data_final = end_date.strftime("%d/%m/%Y") if end_date else date.strftime("%d/%m/%Y")
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4391/dados"
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
        return cdi_obj.iloc[0] / 100 # A API retorna o CDI em percentual, converto para decimal por padrão
    else:
        cdi_list = []
        for idx, row in df.iterrows():
            cdi_list.append({row["data"]: float(row["valor"]) / 100})
        return cdi_list


def get_cdi_range(start_date: datetime, end_date: datetime) -> list[dict[str, float]]:
    cdi_list = []
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados"
    params = {
        "formato": "json",
        "dataInicial": start_date.strftime("%d/%m/%Y"),
        "dataFinal": end_date.strftime("%d/%m/%Y")
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)

    if "erro" in df.columns:
        error = df["erro"]
        raise CdiFetchError(f"Dados de IPCA não encontrados para o campo entre {start_date.strftime('%Y-%m-%d')} e {end_date.strftime('%Y-%m-%d')}: {error}")

    for cdi in df.itertuples():
        cdi_list.append({cdi.data: float(cdi.valor)})
    return cdi_list


def get_yearly_cdi_rate(date: datetime, end_date: datetime=None) -> float | list[dict[str, float]]:
    data_inicial = date.strftime("%d/%m/%Y")
    data_final = end_date.strftime("%d/%m/%Y") if end_date else date.strftime("%d/%m/%Y")
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados"
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
