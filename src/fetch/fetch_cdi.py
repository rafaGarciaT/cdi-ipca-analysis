from datetime import datetime, timedelta
import pandas as pd
import requests


def get_cdi(date: datetime) -> float:
    prev_date = date - timedelta(days=1)
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados"
    params = {
        "formato": "json",
        "dataInicial": prev_date.strftime("%d/%m/%Y"),
        "dataFinal": date.strftime("%d/%m/%Y"),
    }

    response = requests.get(url, params=params)

    data = response.json()
    df = pd.DataFrame(data)
    return df["valor"].astype(float)[0]
