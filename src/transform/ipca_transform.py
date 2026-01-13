import pandas as pd
import json
from pathlib import Path
from typing import List

def load_json(date: str) -> dict[str, float]:
    filepath = Path(f"data/raw/dados_ipca/ipca_{date}.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def get_monthly_ipca_rates(year: str, stop_date: str) -> List[float]:
    project_root = Path(__file__).parent.parent
    base = project_root / "data" / "raw" / "ipca"
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


def calc_accumulated_ipca(ipcas_monthly_rates: List[float], ipca_this_month: float) -> float:
    factor = 1.0
    for ipca in ipcas_monthly_rates:
        factor *= (1 + ipca / 100)

    factor *= (1 + ipca_this_month / 100)
    return round((factor - 1) * 100, 6)
