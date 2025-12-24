from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import requests


def get_ipca(date: datetime) -> float:
    prev_month = date - relativedelta(months=1)
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"
    params = {
        "formato": "json",
        "dataInicial": f"01/{prev_month.strftime('%m/%Y')}",
        "dataFinal": f"02/{date.strftime('%m/%Y')}",
    }

    response = requests.get(url, params=params)

    data = response.json()
    df = pd.DataFrame(data)
    return df["valor"].astype(float)[0]
