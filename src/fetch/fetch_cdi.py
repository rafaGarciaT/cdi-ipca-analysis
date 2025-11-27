import pandas as pd
import requests


def get_cdi(day, month, year):
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados"
    params = {
        "formato": "json",
        "dataInicial": f"{day - 1}/{month}/{year}",
        "dataFinal": f"{day}/{month}/{year}"
    }

    response = requests.get(url, params=params)

    data = response.json()
    df = pd.DataFrame(data)
    return df["valor"].astype(float)[0]
