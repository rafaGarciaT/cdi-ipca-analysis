import json
from datetime import datetime
from pathlib import Path
from typing import List

from src.config import pr_root
from src.storage.raw.base import BaseRawStorage
from src.storage.raw.schema import RawDataPayload


class JsonRawStorage(BaseRawStorage):
    """Gerencia leitura de dados brutos em JSON.

    Attributes:
        data_type (str): Tipo de dado que este armazenamento gerencia, usado para organizar os arquivos JSON.
        base_path (Path): Caminho base onde os arquivos JSON serão armazenados, organizado por tipo de dado.
    """

    def __init__(self, data_type: str) -> None:
        """Inicializa o armazenamento de dados brutos em JSON.

        Attributes:
            data_type (str): Tipo de dado que este armazenamento gerencia, usado para organizar os arquivos JSON.
        """
        self.data_type = data_type
        self.base_path = pr_root / "data" / "raw" / data_type

    def save(self, data: float | dict, reference_date: str) -> str:
        """Salva os dados brutos obtidos em um arquivo JSON.

        Args:
            data (float): Valor dos dados brutos.
            reference_date (str): Data associada aos dados no formato "YYYY-MM".

        Returns:
            str: Caminho do arquivo JSON onde os dados brutos foram salvos.
        """
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
        """Carrega dados brutos para uma data específica.

        Args:
            date (str): Data para a qual os dados brutos devem ser carregados, no formato "YYYY-MM".

        Returns:
            dict[str, float]: Dicionário contendo os dados brutos carregados para a data especificada.
        """

        filepath = self.base_path / f"{self.data_type}_{date}.json"
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_values_until(self, year: str, stop_date: str) -> List[float]:
        """Retorna valores até uma data específica.

        Args:
            year (str): Ano para o qual os valores brutos devem ser obtidos, no formato "YYYY".
            stop_date (str): Data de parada para a obtenção dos valores brutos, no formato "YYYY-MM-DD".

        Returns:
            List[float]: Lista de valores brutos para o ano especificado até a data de parada.
        """
        values = []
        files = sorted(self.base_path.glob(f"{self.data_type}_{year}-*.json"))

        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)
                values.append(data["value"])

            if stop_date in file.name:
                break

        return values

    def get_collected_values(self, raw_dir: Path) -> set:
        """Obtém as datas para as quais os dados brutos já foram coletados. Feito para o Backfill.

        Args:
            raw_dir (Path): Diretório onde os dados brutos estão armazenados.

        Returns:
            set: Conjunto de datas (no formato "YYYY-MM") para as quais os dados brutos já foram coletados.
        """
        processed_dates = set()
        for file in raw_dir.glob("*.json"):
            parts = file.stem.split("_")[-1].split("-")
            if len(parts) == 2:
                year, month = int(parts[0]), int(parts[1])
                processed_dates.add(datetime(year, month, 1))
        return processed_dates