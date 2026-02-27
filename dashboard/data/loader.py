from pathlib import Path
from typing import Literal
import pandas as pd

from dashboard.components.input import render
from src.config import pr_root
from src.storage.processed.factory import ProcessedStorageFactory
from src.storage.processed.schema import cdi_schema, ipca_schema


def _detect_file_format(indicator: str) -> tuple[str, Path] | None:
    """Detecta automaticamente o formato e localização do arquivo de dados processados.

    Args:
        indicator: Nome do indicador ('cdi' ou 'ipca').

    Returns:
        Tupla (formato, caminho) se encontrado, None caso contrário.
    """
    processed_dir = pr_root / "data" / "processed"
    base_name = f"{indicator.lower()}_data"

    # Mapeamento de extensões para formatos de storage
    format_map = {
        ".xlsx": "excel",
        ".xls": "excel",
        ".csv": "csv",
    }

    for ext, fmt in format_map.items():
        filepath = processed_dir / f"{base_name}{ext}"
        if filepath.exists():
            return fmt, filepath

    return None


def load_indicator_data(indicator: Literal["cdi", "ipca"]) -> pd.DataFrame:
    """Carrega dados processados de um indicador, detectando automaticamente o formato do arquivo.

    Args:
        indicator: Nome do indicador ('cdi' ou 'ipca').

    Returns:
        DataFrame com os dados processados do indicador, ordenados por data.

    Raises:
        FileNotFoundError: Se nenhum arquivo de dados processados for encontrado.
        ValueError: Se o indicador não for reconhecido.
    """
    valid_indicators = ["cdi", "ipca"]
    if indicator.lower() not in valid_indicators:
        raise ValueError(
            f"Indicador inválido: {indicator}. "
            f"Use um dos seguintes: {', '.join(valid_indicators)}"
        )

    detected = _detect_file_format(indicator)
    if detected is None:
        raise FileNotFoundError(
            f"Nenhum arquivo de dados processados encontrado para {indicator}. "
            f"Procurado em: {pr_root / 'data' / 'processed'}"
        )

    file_format, filepath = detected
    schema_map = {"cdi": cdi_schema, "ipca": ipca_schema}

    storage = ProcessedStorageFactory.create_storage(
        file_format,
        filepath,
        schema_map[indicator.lower()]
    )

    df = storage.get_data()
    df["date"] = pd.to_datetime(df["date"])
    return df.sort_values("date").reset_index(drop=True)


def load_all_indicators() -> dict[str, pd.DataFrame]:
    """Carrega dados processados de todos os indicadores disponíveis, detectando automaticamente os formatos.

    Returns:Dicionário com os dados de cada indicador, onde as chaves são os nomes dos indicadores.
    """
    indicators = ["cdi", "ipca"]
    data = {}

    for indicator in indicators:
        try:
            data[indicator] = load_indicator_data(indicator)
        except FileNotFoundError:
            continue

    return data


def get_latest_values() -> dict[str, dict]:
    """Obtém os valores mais recentes de todos os indicadores disponíveis.

    Returns:
        Dicionário com os valores mais recentes de cada indicador.
    """
    all_data = load_all_indicators()
    latest = {}

    for indicator, df in all_data.items():
        if not df.empty:
            latest_row = df.iloc[-1]
            latest[indicator] = latest_row.to_dict()

    return latest


def filter_by_period(
    df: pd.DataFrame,
    start_date: str | pd.Timestamp,
    end_date: str | pd.Timestamp | None = None
) -> pd.DataFrame:
    """Filtra um DataFrame por período específico.

    Args:
        df: DataFrame com os dados processados.
        start_date: Data inicial do período.
        end_date: Data final do período. Se None, considera até a data mais recente.

    Returns:
        DataFrame filtrado pelo período especificado.
    """
    df = df.copy()
    df["date"] = pd.to_datetime(df["date"])

    start = pd.to_datetime(start_date)
    mask = df["date"] >= start

    if end_date is not None:
        end = pd.to_datetime(end_date)
        mask &= df["date"] <= end

    return df[mask].reset_index(drop=True)


def get_ytd_data(
    indicator: Literal["cdi", "ipca"],
    year: int | None = None
) -> pd.DataFrame:
    """Obtém dados do ano até a data atual (Year-to-Date) para um indicador.

    Args:
        indicator: Nome do indicador ('cdi' ou 'ipca').
        year: Ano específico. Se None, usa o ano atual.

    Returns:
        DataFrame com os dados YTD do indicador.
    """
    df = load_indicator_data(indicator)
    target_year = year or pd.Timestamp.now().year

    df["date"] = pd.to_datetime(df["date"])
    return df[df["date"].dt.year == target_year].reset_index(drop=True)


def get_last_n_months(
    indicator: Literal["cdi", "ipca"],
    n: int
) -> pd.DataFrame:
    """Obtém os dados dos últimos N meses para um indicador.

    Args:
        indicator: Nome do indicador ('cdi' ou 'ipca').
        n: Número de meses a retornar.

    Returns:
        DataFrame com os dados dos últimos N meses.
    """
    df = load_indicator_data(indicator)
    return df.tail(n).reset_index(drop=True)


def get_available_indicators() -> list[str]:
    """Lista todos os indicadores que possuem dados processados disponíveis.

    Returns:
        Lista de nomes de indicadores com dados disponíveis.
    """
    indicators = ["cdi", "ipca"]
    available = []

    for indicator in indicators:
        if _detect_file_format(indicator) is not None:
            available.append(indicator)

    return available


def get_indicator_info(indicator: Literal["cdi", "ipca"]) -> dict:
    """Obtém informações sobre o arquivo de dados de um indicador.

    Args:
        indicator: Nome do indicador ('cdi' ou 'ipca').

    Returns:
        Dicionário com informações sobre o arquivo (formato, caminho, tamanho, etc.).

    Raises:
        FileNotFoundError: Se nenhum arquivo for encontrado para o indicador.
    """
    detected = _detect_file_format(indicator)
    if detected is None:
        raise FileNotFoundError(f"Nenhum arquivo encontrado para {indicator}")

    file_format, filepath = detected

    return {
        "indicator": indicator,
        "format": file_format,
        "filepath": str(filepath),
        "file_size_kb": filepath.stat().st_size / 1024,
        "exists": filepath.exists()
    }


"""

Exemplos de uso

from dashboards.load import (
    load_indicator_data,
    load_all_indicators,
    get_available_indicators,
    get_indicator_info
)

# Carrega automaticamente o formato correto
cdi_data = load_indicator_data("cdi")  # Funciona com .xlsx, .csv, etc.

# Ver quais indicadores estão disponíveis
available = get_available_indicators()
print(f"Indicadores disponíveis: {available}")

# Obter informações sobre o arquivo
info = get_indicator_info("cdi")
print(f"Formato: {info['format']}, Tamanho: {info['file_size_kb']:.2f} KB")

# Carregar todos os indicadores disponíveis
all_data = load_all_indicators()


"""