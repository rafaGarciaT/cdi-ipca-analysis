from src.fetch.fetch_cdi import get_cdi
from src.fetch.fetch_ipca import get_ipca
from src.utils.date_utils import date_info, is_business_day
import json
from pathlib import Path


class Pipeline:
    def __init__(self, persistence_mode="excel"):
        self.persistence_mode = persistence_mode

        self.loaders = {
            "excel": self._load_to_excel,
            "sqlite": self._load_to_sqlite
        }

    def run(self):
        print("=== INICIANDO PIPELINE ===>")

        print("> Preparando...") # -------- PREPARE --------

        dt = self._fetch_date()

        if is_business_day(dt) is False:
            print("Data informada não é um dia útil. Encerrando pipeline.")


        day = dt.day
        month = dt.month
        year = dt.year

        # todo: validar se data já foi processada

        print("> Buscando dados...") # -------- FETCH --------

        dados_cdi = self._fetch_cdi(day, month, year)
        fpath_cdi = self._save_raw(dados_cdi, "cdi", day, month, year)

        dados_ipca = self._fetch_ipca(month, year)
        fpath_ipca = self._save_raw(dados_ipca, "dados_ipca", day, month, year)

        print("> Processando e calculando...") # -------- TRANSFORM --------
        rentabilidade = self._transform(dados_cdi)
        inflacao = self._transform(dados_ipca)

        print("> Salvando resultados...") # -------- LOAD --------
        self._load(rentabilidade)

        print("=== PIPELINE FINALIZADA ===")

    # ============================
    #  FETCH
    # ============================

    def _fetch_date(self):
        return date_info()


    def _fetch_cdi(self, day, month, year):
        return get_cdi(day, month, year) # float


    def _fetch_ipca(self, month, year):
        return get_ipca(month, year) # float


    def _save_raw(self, data, name, day, month, year):
        pr_root = Path(__file__).parent.parent
        folder = pr_root / "data" / "raw" / name
        folder.mkdir(parents=True, exist_ok=True)

        filepath = folder / f"{name}_{year}-{month}-{day}.json"

        payload = {
            "date": f"{year}-{month}-{day}",
            "type": name,
            "value": data
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        return str(filepath)

    # ============================
    #  TRANSFORM
    # ============================

    def _transform(self, dados_cdi):
        # TODO: implementar transform
        return

    # ============================
    #  LOAD
    # ============================

    def _load(self, resultado):
        self.loaders[self.persistence_mode](resultado)
        return

    def _load_to_excel(self, resultado):
        # TODO: implementar persistência em excel
        return

    def _load_to_sqlite(self, resultado):
        # TODO: implementar persistência em sqlite
        return
