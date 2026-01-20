from datetime import datetime
from src.config import API_DATE_FORMAT, API_BASE_URL_IPCA_MONTHLY
import pandas as pd
import requests


class IpcaFetchError(Exception):
    pass


def get_monthly_ipca(date: datetime, end_date: datetime=None) -> float | list[dict[str, float]]:
    """Retorna uma, ou uma lista de taxas de IPCA mensais para o período especificado."""
    data_inicial = date.strftime(API_DATE_FORMAT)
    data_final = end_date.strftime(API_DATE_FORMAT) if end_date else date.strftime(API_DATE_FORMAT)
    url = API_BASE_URL_IPCA_MONTHLY
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
        raise IpcaFetchError(f"Dados de IPCA não encontrados para a data {date.strftime('%Y-%m-%d')}: {error}")

    ipca_obj = df["valor"].astype(float)
    if len(ipca_obj) == 1:
        return ipca_obj.iloc[0]
    else:
        ipca_list = []
        for idx, row in df.iterrows():
            ipca_list.append({row["data"]: float(row["valor"])})
        return ipca_list
