from datetime import datetime, timedelta
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

    for cdi in df.itertuples():
        cdi_list.append({cdi.data: float(cdi.valor)})
    return cdi_list
