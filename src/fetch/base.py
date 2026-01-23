from datetime import datetime
from src.config import BCB_API_DATE_FORMAT
import pandas as pd
import requests


def fetch_bcb_data(url: str, date: datetime, end_date: datetime = None, error_class: type[Exception] = Exception) -> float | list[dict[str, float]]:
    """Fetcher genérico para a API da BCB."""
    data_inicial = date.strftime(BCB_API_DATE_FORMAT)
    data_final = end_date.strftime(BCB_API_DATE_FORMAT) if end_date else date.strftime(BCB_API_DATE_FORMAT)

    params = {
        "formato": "json",
        "dataInicial": data_inicial,
        "dataFinal": data_final
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        raise error_class(f"Falha no fetch: {str(e)}")

    df = pd.DataFrame(data)

    if df.empty or "erro" in df.columns:
        error = df["erro"].iloc[0] if "erro" in df.columns else "Nenhum valor"
        raise error_class(f"Dados não encontrados para {date.strftime('%Y-%m-%d')}: {error}")

    df["valor"] = df["valor"].astype(float)

    if len(df) == 1:
        return df["valor"].iloc[0]
    else:
        obj_list = []
        for idx, row in df.iterrows():
            obj_list.append({row["data"]: float(row["valor"])})
        return obj_list
