import json
from pathlib import Path
from typing import List
from src.config import pr_root


def load_json(date: str) -> dict[str, float]:
    """Carrega os dados brutos CDI em JSON para uma data em específico."""
    filepath = Path(f"data/raw/dados_ipca/cdi_{date}.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_annual_cdi_rates(year: str, stop_date: str) -> List[float]:
    """Retorna uma lista com as taxas CDI anuais até uma certa data."""
    base = pr_root / "data" / "raw" / "cdi"
    cdi_list = []

    files = sorted(base.glob(pattern=f"cdi_{year}-*.json"))
    names = [p.name for p in files]
    for n in names:
        if stop_date in n:
            break
        filepath = base / n
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            cdi_list.append(data["value"])

    return cdi_list


def calc_accumulated_cdi(cdi_annual_rates: List[float]) -> float:
    """Calcula o CDI acumulado a partir de uma lista de taxas CDI anuais."""
    factor = 1.0
    for rate in cdi_annual_rates:
        factor *= calc_cdi_daily_factor(rate)
    return factor - 1


def calc_cdi_daily_factor(cdi_annual_rate: float) -> float:
    """Calcula o fator diário do CDI a partir da taxa anual."""
    return (1 + cdi_annual_rate) ** (1 / 252)
