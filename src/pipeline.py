from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
from src.fetch.fetch_cdi import get_cdi, get_cdi_range, CdiFetchError, get_monthly_cdi_rate, get_yearly_cdi_rate
from src.fetch.fetch_ipca import get_monthly_ipca, IpcaFetchError
from src.utils.date_utils import date_info, is_business_day
from src.transform.cdi_transform import calc_accumulated_cdi, get_annual_cdi_rates, calc_cdi_daily_factor
from src.transform.ipca_transform import get_monthly_ipca_rates, calc_accumulated_ipca
from src.storage.excel_ipca import register_ipca_data, get_last_ipca_accumulated
from src.storage.excel_cdi import register_cdi_data, get_last_cdi_accumulated
import json
from pathlib import Path


class Pipeline:
    def __init__(self, persistence_mode="excel", execution_mode="daily", target_year=None):
        self.persistence_mode = persistence_mode
        self.execution_mode = execution_mode
        self.target_year = target_year if target_year else datetime.now().year

        # Desabilitado por enquanto para encaixar melhor com os loaders específicos para cada dado
        # self.loaders = {
        #     "excel": self._load_to_excel,
        #     "sqlite": self._load_to_sqlite
        # }
    # ============================
    #  RUN
    # ============================

    def run(self):
        print("=== INICIANDO PIPELINE ===")
        print(f"Modo de execução: {self.execution_mode}\n> Preparando...")

        dt = self._fetch_date()

        if self.execution_mode == "daily": self._run_daily(dt)
        elif self.execution_mode == "yearly": self._run_yearly(dt)
        elif self.execution_mode == "backfill": self._run_backfill(dt)
        else:
            print(f"Modo desconhecido: {self.execution_mode}")

        print("=== PIPELINE FINALIZADA ===")


    def _run_daily(self, dt):
        if not is_business_day(dt):
            print("Data informada não é um dia útil. Encerrando pipeline.")
            return

        if self._cdi_has_been_processed(dt):
            print("Data já foi processada. Encerrando pipeline.")
            return

        if self._ipca_has_been_processed(dt):
            print("Data já foi processada. Encerrando pipeline.")
            return

        print("> Buscando dados...")
        dados_cdi, yearly_cdi = self._fetch_cdi(dt)
        self._save_raw(dados_cdi, "monthly_cdi", dt)
        self._save_raw(yearly_cdi, "yearly_cdi", dt)

        dados_ipca, yearly_cdi = self._fetch_ipca(dt)
        self._save_raw(dados_ipca, "ipca", dt)

        print("> Processando e calculando...")
        cdi_dict = self._transform_cdi(dados_cdi, dt)
        ipca_dict = self._transform_ipca(dados_ipca, dt)

        print("> Salvando resultados...")
        self._load_cdi_to_excel(cdi_dict)
        self._load_ipca_to_excel(ipca_dict)


    def _run_yearly(self, dt):
        print(f"> Recolhendo dados do ano {self.target_year}...\n")
        year = self.target_year

        start_date = datetime(year, 1, 1)
        end_date = min(datetime(year, 12, 31), dt)

        print("> Buscando dados...")
        try:
            cdi_data, yearly_cdi = self._fetch_cdi(start_date, end_date)
        except Exception as e:
            print(f"Erro ao buscar dados de CDI: {e}")
        try:
            ipca_data = self._fetch_ipca(start_date, end_date)
        except Exception as e:
            print(f"Erro ao buscar dados de IPCA: {e}")

        print("> Processando e salvando dados (CDI)...")
        for cdi_entry, cdi_yearly_entry in zip(cdi_data, yearly_cdi):
            for date_str, value in cdi_entry.items():
                date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                yearly_value = next(iter(cdi_yearly_entry.values()))

                if not self._cdi_has_been_processed(date_obj):
                    self._save_raw(value, "monthly_cdi", date_obj)
                    self._save_raw(yearly_value, "yearly_cdi", date_obj)
                    cdi_dict = self._transform_cdi(value, yearly_value, date_obj)
                    self._load_cdi_to_excel(cdi_dict)

        print("> Processando e salvando dados (IPCA)...")
        for ipca_entry in ipca_data:
            for date_str, value in ipca_entry.items():
                date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                month, year_val = date_obj.month, date_obj.year

                if not self._ipca_has_been_processed(date_obj):
                    self._save_raw(value / 100, "ipca", date_obj)
                    ipca_dict = self._transform_ipca(value / 100, date_obj)
                    self._load_ipca_to_excel(ipca_dict)


    def _run_backfill(self, dt):
        pr_root = Path(__file__).parent.parent
        cdi_raw_dir = pr_root / "data" / "raw" / "cdi"
        ipca_raw_dir = pr_root / "data" / "raw" / "ipca"

        if not cdi_raw_dir.exists() or not ipca_raw_dir.exists():
            print("Nenhum dado bruto encontrado.")
            return

        cdi_processed_dates = set()
        for file in cdi_raw_dir.glob("*.json"):
            cdi_parts = file.stem.split("_")[1].split("-")  # Extrai a data do nome do arquivo: cdi_YYYY-MM-DD.json
            if len(cdi_parts) == 2:
                cdi_processed_dates.add(datetime(int(cdi_parts[0]), int(cdi_parts[1]), 1))

        ipca_processed_dates = set()
        for file in ipca_raw_dir.glob("*.json"):
            ipca_parts = file.stem.split("_")[1].split("-")
            if len(ipca_parts) == 2:
                ipca_processed_dates.add(datetime(int(ipca_parts[0]), int(ipca_parts[1]), 1))

        if not cdi_processed_dates or not ipca_processed_dates:
            print("Dados insuficientes para backfill.")
            return

        cdi_min_date, cdi_max_date = min(cdi_processed_dates), max(cdi_processed_dates)
        ipca_min_date, ipca_max_date = min(ipca_processed_dates), max(ipca_processed_dates)

        filled_count = 0

        print(f"CDI - Preenchendo lacunas entre {cdi_min_date.date()} e {cdi_max_date.date()}...")
        print(f"IPCA - Preenchendo lacunas entre {ipca_min_date.date()} e {ipca_max_date.date()}...")
        print(">Buscando dados...")
        cdi_data, yearly_cdi = self._fetch_cdi(cdi_min_date, cdi_max_date)
        ipca_data = self._fetch_ipca(ipca_min_date, ipca_max_date)

        print("> Processando e salvando dados (CDI)...")
        if cdi_data:
            for cdi_entry, cdi_yearly_entry in zip(cdi_data, yearly_cdi):
                for date_str, value in cdi_entry.items():
                    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                    yearly_value = next(iter(cdi_yearly_entry.values()))

                    if is_business_day(date_obj) and date_obj not in cdi_processed_dates:
                        self._save_raw(value, "monthly_cdi", date_obj)
                        self._save_raw(yearly_value, "yearly_cdi", date_obj)
                        cdi_dict = self._transform_cdi(value, yearly_value, date_obj)
                        self._load_cdi_to_excel(cdi_dict)
                        filled_count += 1
        else:
            print("Nenhum dado de CDI disponível para backfill.")

        print("> Processando e salvando dados (IPCA)...")
        if ipca_data:
            for ipca_entry in ipca_data:
                for date_str, value in ipca_entry.items():
                    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
                    month_start = datetime(date_obj.year, date_obj.month, 1)

                    if month_start not in ipca_processed_dates:
                        self._save_raw(value / 100, "ipca", date_obj)
                        ipca_dict = self._transform_ipca(value / 100, date_obj)
                        self._load_ipca_to_excel(ipca_dict)
                        filled_count += 1
        else:
            print("Nenhum dado de IPCA disponível para backfill.")

        print(f"Total de datas preenchidas: {filled_count}")






    # ============================
    #  PREPARE
    # ============================

    def _cdi_has_been_processed(self, dt):
        pr_root = Path(__file__).parent.parent
        filepath = pr_root / "data" / "raw" / "cdi" / f"cdi_{dt.strftime("%Y-%m")}.json"
        return filepath.exists()


    def _ipca_has_been_processed(self, dt):
        pr_root = Path(__file__).parent.parent
        filepath = pr_root / "data" / "raw" / "ipca" / f"ipca_{dt.strftime("%Y-%m")}.json"
        return filepath.exists()

    # ============================
    #  FETCH
    # ============================

    def _fetch_date(self):
        return date_info()


    def _fetch_cdi(self, datetime, end_datetime=None):
        return get_monthly_cdi_rate(datetime, end_datetime), get_yearly_cdi_rate(datetime, end_datetime)


    def _fetch_ipca(self, datetime, end_datetime=None):
        return get_monthly_ipca(datetime, end_datetime)


    def _save_raw(self, data, name, dt):
        pr_root = Path(__file__).parent.parent
        folder = pr_root / "data" / "raw" / name
        folder.mkdir(parents=True, exist_ok=True)

        if name == "monthly_cdi":
            filepath = folder / f"{name}_{dt.strftime("%Y-%m")}.json"

            payload = {
                "reference_date": f"{dt.strftime("%Y-%m")}",
                "type": name,
                "value": data  # A API retorna a taxa anual do CDI em float
            }

        elif name == "yearly_cdi":
            filepath = folder / f"{name}_{dt.strftime("%Y-%m")}.json"

            payload = {
                "reference_date": f"{dt.strftime("%Y-%m")}",
                "type": name,
                "value": data  # A API retorna a taxa anual do CDI em float
            }

        elif name == "ipca":
            filepath = folder / f"{name}_{dt.strftime("%Y-%m")}.json"

            payload = {
                "reference_date": f"{dt.strftime("%Y-%m")}",
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

    def _transform_cdi(self, dados_cdi, dados_cdi_anual, dt):
        # last_accumulated_cdi = get_last_cdi_accumulated(dt)
        cdi_annual_rates = get_annual_cdi_rates(dt.year, f"{dt.strftime("%Y-%m-%d")}")
        cdi_daily_factor = calc_cdi_daily_factor(dados_cdi)
        # accumulated_cdi = (1 + last_accumulated_cdi) * cdi_daily_factor - 1
        # return {"year": f"{dt.year}", "month": f"{dt.month}", "cdi_annual_rate": dados_cdi_anual, "cdi_daily_factor": cdi_daily_factor, "cdi_monthly_rate": dados_cdi, "cdi_accumulated": accumulated_cdi}
        return {"year": f"{dt.year}", "month": f"{dt.month}", "cdi_annual_rate": dados_cdi_anual, "cdi_monthly_rate": dados_cdi}

    def _transform_ipca(self, dados_ipca, dt):
        # last_accumulated_ipca = get_last_ipca_accumulated(dt)
        ipca_monthly_rates = get_monthly_ipca_rates(dt.year, f"{dt.strftime("%Y-%m")}")
        # accumulated_ipca = (1 + last_accumulated_ipca) * (1 + dados_ipca) - 1
        # return {"date": f"{dt.strftime("%Y-%m")}", "ipca_monthly_rate": dados_ipca,"ipca_accumulated": accumulated_ipca}

        return {"date": f"{dt.strftime("%Y-%m")}", "ipca_monthly_rate": dados_ipca}

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
