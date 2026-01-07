from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import requests


class IpcaFetchError(Exception):
    pass

def get_ipca(date: datetime) -> float:
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
    params = {
        "formato": "json",
        "dataInicial": f"{date.strftime('%d/%m/%Y')}",
        "dataFinal": f"{date.strftime('%d/%m/%Y')}",
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)

    if "erro" in df.columns:
        error = df["erro"]
        raise IpcaFetchError(f"Dados de IPCA não encontrados para a data {date.strftime('%Y-%m-%d')}: {error}")

    return df["valor"].astype(float).iloc[0]

def get_ipca_range(start_date: datetime, end_date: datetime) -> list[dict[str, float]]:
    ipca_list = []
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
    params = {
        "formato": "json",
        "dataInicial": start_date.strftime("%d/%m/%Y"),
        "dataFinal": end_date.strftime("%d/%m/%Y")
    }
    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)

    for ipca in df.itertuples():
        ipca_list.append({ipca.data: float(ipca.valor)})
    return ipca_list
