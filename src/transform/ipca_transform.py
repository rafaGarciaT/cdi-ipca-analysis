import json
from pathlib import Path
from typing import List
from src.config import pr_root


def load_json(date: str) -> dict[str, float]:
    """Carrega os dados brutos CDI em JSON para uma data em específico."""
    filepath = Path(f"data/raw/dados_ipca/ipca_{date}.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def get_monthly_ipca_rates(year: str, stop_date: str) -> List[float]:
    """Retorna uma lista com as taxas IPCA mensais até uma certa data."""
    base = pr_root / "data" / "raw" / "ipca"
    ipca_list = []

    files = sorted(base.glob(pattern=f"ipca_{year}-*.json"))
    names = [p.name for p in files]
    for n in names:
        if stop_date in n:
            break
        filepath = base / n
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            ipca_list.append(data["value"])

    return ipca_list


def calc_accumulated_ipca(ipca_monthly_rates: List[float], ipca_this_month: float) -> float:
    """Calcula o IPCA acumulado a partir de uma lista de taxas IPCA mensais."""
    factor = 1.0
    for ipca in ipca_monthly_rates:
        factor *= (1 + ipca / 100)

    factor *= (1 + ipca_this_month / 100)
    return round((factor - 1) * 100, 6)
