from src.fetch.fetch_cdi import get_cdi
from src.fetch.fetch_ipca import get_ipca
from src.utils.date_utils import date_info, is_business_day
from src.transform.cdi_transform import calc_annual_cdi, get_annual_cdi
from src.transform.ipca_transform import calc_annual_ipca, get_annual_ipca
from src.load.load_to_excel import register_cdi_data, register_ipca_data
import json
from pathlib import Path


class Pipeline:
    def __init__(self, persistence_mode="excel"):
        self.persistence_mode = persistence_mode

        # Desabilitado por enquanto para encaixar melhor com os loaders específicos para cada dado
        # self.loaders = {
        #     "excel": self._load_to_excel,
        #     "sqlite": self._load_to_sqlite
        # }


    def run(self):
        print("=== INICIANDO PIPELINE ===>")

        print("> Preparando...") # -------- PREPARE --------

        dt = self._fetch_date()

        if is_business_day(dt) is False:
            print("Data informada não é um dia útil. Encerrando pipeline.")

        day, month, year = dt.day, dt.month, dt.year

        # todo: validar se data já foi processada

        print("> Buscando dados...") # -------- FETCH --------

        dados_cdi = self._fetch_cdi(dt)
        fpath_cdi = self._save_raw(dados_cdi, "cdi", day, month, year)

        dados_ipca = self._fetch_ipca(dt)
        fpath_ipca = self._save_raw(dados_ipca, "ipca", day, month, year)

        print("> Processando e calculando...") # -------- TRANSFORM --------
        cdi_dict = self._transform_cdi(dados_cdi, year, month, day)
        ipca_dict = self._transform_ipca(dados_ipca, year, month)

        print("> Salvando resultados...") # -------- LOAD --------
        self._load(cdi_dict)
        self._load(ipca_dict)

        print("=== PIPELINE FINALIZADA ===")

    # ============================
    #  FETCH
    # ============================

    def _fetch_date(self):
        return date_info()


    def _fetch_cdi(self, datetime):
        return get_cdi(datetime) # float


    def _fetch_ipca(self, datetime):
        return get_ipca(datetime) # float


    def _save_raw(self, data, name, day, month, year):
        pr_root = Path(__file__).parent.parent
        folder = pr_root / "data" / "raw" / name
        folder.mkdir(parents=True, exist_ok=True)

        if name == "cdi":
            filepath = folder / f"{name}_{year}-{month}-{day}.json"

            payload = {
                "date": f"{year}-{month}-{day}",
                "type": name,
                "value": data
            }
        elif name == "ipca":
            filepath = folder / f"{name}_{year}-{month}.json"

            payload = {
                "date": f"{year}-{month}-{day}",
                "type": name,
                "value": data
            }
        else:
            raise ValueError("Nome inválido para salvar dados brutos.")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        return str(filepath)

    # ============================
    #  TRANSFORM
    # ============================

    def _transform_cdi(self, dados_cdi, year, month, day):
        cdis_so_far = get_annual_cdi(year, f"{year}-{month}-{day}")
        annual_cdi = calc_annual_cdi(cdis_so_far, dados_cdi)
        return {"date": f"{year}-{month}-{day}", "cdi_daily": dados_cdi, "cdi_annual": annual_cdi}

    def _transform_ipca(self, dados_ipca, year, month):
        ipcas_so_far = get_annual_ipca(year, f"{year}-{month}")
        annual_ipca = calc_annual_ipca(ipcas_so_far, dados_ipca)
        return {"date": f"{year}-{month}", "ipca_monthly": dados_ipca, "ipca_annual": annual_ipca}

    # ============================
    #  LOAD
    # ============================

    # Desabilitado por enquanto para encaixar melhor com os loaders específicos para cada dado
    # def _load(self, new_row):
    #     self.loaders[self.persistence_mode](new_row)
    #     return

    def _load_cdi_to_excel(self, new_row):
        register_cdi_data(new_row)


    def _load_ipca_to_excel(self, new_row):
        register_ipca_data(new_row)


    def _load_to_sqlite(self, new_row):
        # TODO: implementar persistência em sqlite
        return
