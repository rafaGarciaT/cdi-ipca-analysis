import pandas as pd
import json
from pathlib import Path
from typing import List

def load_json(date: str) -> dict[str, float]:
    filepath = Path(f"data/raw/dados_ipca/ipca_{date}.json")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def get_annual_ipca(year: str, today: str) -> List[float]:
    project_root = Path(__file__).parent.parent
    base = project_root / "data" / "raw" / "ipca"
    ipca_list = []

    files = sorted(base.glob(pattern=f"ipca_{year}-*.json"))
    names = [p.name for p in files]
    for n in names:
        if today in n:
            break
        filepath = base / n
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            ipca_list.append(data["value"])

    return ipca_list


def calc_annual_ipca(ipcas_so_far: List[float], ipca_today: float) -> float:
    factor = 1.0

    for ipca in ipcas_so_far:
        factor *= (1 + ipca / 100)

    factor *= (1 + ipca_today / 100)

    return round((factor - 1) * 100, 6)


def calc_ipca_acumulado(valores: list[float]) -> float:
    serie = pd.Series(valores)
    return (1 + serie / 100).prod() - 1