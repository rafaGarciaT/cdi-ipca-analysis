import pandas as pd
import requests


def get_ipca( month, year):
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
    params = {
        "formato": "json",
        "dataInicial": f"01/{month - 1}/{year}",
        "dataFinal": f"02/{month}/{year}"
    }

    response = requests.get(url, params=params)

    data = response.json()
    df = pd.DataFrame(data)
    return df["valor"].astype(float)[0]
