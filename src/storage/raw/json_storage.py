import json
from typing import List
from src.config import pr_root
from src.storage.raw.schema import RawDataPayload


class JsonRawStorage:
    """Gerencia leitura de dados brutos em JSON."""

    def __init__(self, data_type: str):
        self.data_type = data_type
        self.base_path = pr_root / "data" / "raw" / data_type

    def save(self, data: float, reference_date: str) -> str:
        """Salva os dados brutos obtidos em um arquivo JSON."""
        self.base_path.mkdir(parents=True, exist_ok=True)

        filepath = self.base_path / f"{self.data_type}_{reference_date}.json"

        payload: RawDataPayload = {
            "reference_date": reference_date,
            "type": self.data_type,
            "value": data
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        return str(filepath)

    def load(self, date: str) -> dict[str, float]:
        """Carrega dados brutos para uma data específica."""
        filepath = self.base_path / f"{self.data_type}_{date}.json"
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_values_until(self, year: str, stop_date: str) -> List[float]:
        """Retorna valores até uma data específica."""
        values = []
        files = sorted(self.base_path.glob(f"{self.data_type}_{year}-*.json"))

        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                values.append(data["value"])

            if stop_date in file.name:
                break

        return values