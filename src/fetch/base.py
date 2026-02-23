from datetime import datetime
from src.config import BCB_API_DATE_FORMAT
import pandas as pd
import requests


def fetch_bcb_data(url: str, date: datetime, end_date: datetime = None, error_class: type[Exception] = Exception) -> float | list[dict[str, float]]:
    """Busca dados de séries temporais da API do Banco Central do Brasil. Fetcher genérico.

    Faz requisição HTTP para a API do BCB e retorna os valores da série temporal
    no período especificado. Suporta tanto consultas de data única quanto intervalos.

    Args:
        url (str): URL completa da série temporal do BCB.
        date (datetime): Data inicial (ou única) da consulta.
        end_date (datetime, optional): Data final da consulta. Se None, consulta apenas
            a data inicial. Defaults to None.
        error_class (type[Exception], optional): Classe de exceção a ser lançada em caso
            de erro. Defaults to Exception.

    Returns:
        obj_list (float | list[dict[str, float]]): Se consulta de data única, retorna float com o valor.
            Se intervalo de datas, retorna lista de dicionários {data: valor}.

    Raises:
        error_class: Quando ocorre falha na requisição HTTP.
        error_class: Quando não há dados disponíveis para o período.

    Note:
        - A API do BCB usa formato de data DD/MM/YYYY. Formato presente na constante BCB_API_DATE_FORMAT em src/config.
        - Timeout padrão de 10 segundos para requisições
        - Valores são convertidos automaticamente para float
    """

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
