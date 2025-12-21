import json
from pathlib import Path
from typing import Any, TypeAlias, List


def load_json(date: str) -> dict[str, float]:
    filepath = Path(f"data/raw/dados_ipca/cdi_{date}.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def get_annual_cdi(year: str, today: str) -> List[float]:
    project_root = Path(__file__).parent.parent
    base = project_root / "data" / "raw" / "cdi"
    cdi_list = []

    files = sorted(base.glob(pattern=f"cdi_{year}-*.json"))
    names = [p.name for p in files]
    for n in names:
        if today in n:
            break
        filepath = base / n
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            cdi_list.append(data["value"])

    return cdi_list

def calc_annual_cdi(cdis_so_far: List[float], cdi_today: float) -> float:
    factor = 1.0

    for cdi in cdis_so_far:
        factor *= (1 + cdi / 100)

    factor *= (1 + cdi_today / 100)

    return round((factor - 1) * 100, 6)

def calc_cdi_anual(cdi_diario: float) -> float:
    return round(((1 + cdi_diario / 100) ** 252 - 1) * 100, 6)