from datetime import datetime
from src.fetch.fetch_cdi import get_monthly_cdi_rate, get_yearly_cdi_rate
from src.fetch.fetch_ipca import get_monthly_ipca
from src.utils.date_utils import date_info, is_business_day
from src.config import pr_root, API_DATE_FORMAT
from src.storage.excel_ipca import register_ipca_data
from src.storage.excel_cdi import register_cdi_data
import json
from typing import TypeAlias

fetchReturns: TypeAlias = float | list[dict[str, float]]

class Pipeline:
    def __init__(self, persistence_mode: str = "excel", execution_mode: str = "month", target_year: str = None):
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

        if self.execution_mode == "month": self._run_month(dt)
        elif self.execution_mode == "yearly": self._run_year(dt)
        elif self.execution_mode == "backfill": self._run_backfill()
        else:
            print(f"Modo desconhecido: {self.execution_mode}")

        print("=== PIPELINE FINALIZADA ===")


    def _run_month(self, dt: datetime):
        if not is_business_day(dt):
            print("Data informada não é um dia útil. Encerrando pipeline.")
            return

        if self._ipca_has_been_processed(dt):
            print("Data já foi processada. Encerrando pipeline.")
            return

        print("> CDI\nBuscando dados...")
        if self._cdi_has_been_processed(dt):
            print("CDI já foi processado nessa data já foi processada. Encerrando passo CDI.")
        else:
            monthly_cdi = yearly_cdi = None

            try:
                monthly_cdi, yearly_cdi = self._fetch_cdi(dt)
            except Exception as e:
                print(f"Erro ao buscar dados de CDI, encerrando passo CDI. Exception: {e}")

            if monthly_cdi is not None or yearly_cdi is not None:
                try:
                    print("Processando e salvando dados...")
                    self._save_raw(monthly_cdi, "monthly_cdi", dt)
                    self._save_raw(yearly_cdi, "yearly_cdi", dt)
                    cdi_dict = self._transform_cdi(monthly_cdi, yearly_cdi, dt)

                    self._load_cdi_to_excel(cdi_dict)
                except Exception as e:
                    print(f"Erro ao processar dados de CDI, encerrando passo CDI. Exception: {e}")

        print("> IPCA\nBuscando dados...")
        if self._ipca_has_been_processed(dt):
            print("IPCA já foi processado nessa data já foi processada. Encerrando passo IPCA.")
        else:
             monthly_ipca = None
             try:
                monthly_ipca = self._fetch_ipca(dt)
             except Exception as e:
                print(f"Erro ao buscar dados de IPCA, encerrando passo IPCA. Exception: {e}")

             if monthly_ipca is not None:
                try:
                    self._save_raw(monthly_ipca, "ipca", dt)
                    ipca_dict = self._transform_ipca(monthly_ipca, dt)

                    self._load_ipca_to_excel(ipca_dict)
                except Exception as e:
                    print(f"Erro ao processar dados de IPCA, encerrando passo IPCA. Exception: {e}")


    def _run_year(self, dt: datetime):
        print(f"> Recolhendo dados do ano {self.target_year}...\n")
        year = self.target_year

        start_date = datetime(year, 1, 1)
        end_date = min(datetime(year, 12, 31), dt)

        print("> Buscando dados...")
        cdi_data = yearly_cdi = ipca_data = []

        try:
            cdi_data, yearly_cdi = self._fetch_cdi(start_date, end_date)
        except Exception as e:
            print(f"Erro ao buscar dados de CDI, encerrando passo CDI. Exception: {e}")
            cdi_data = yearly_cdi = []

        try:
            ipca_data = self._fetch_ipca(start_date, end_date)
        except Exception as e:
            print(f"Erro ao buscar dados de IPCA, encerrando passo IPCA. Exception: {e}")
            ipca_data = []

        print("> Processando e salvando dados (CDI)...")
        try:
            for cdi_entry, cdi_yearly_entry in zip(cdi_data, yearly_cdi):
                for date_str, value in cdi_entry.items():
                    date_obj = datetime.strptime(date_str, API_DATE_FORMAT)
                    yearly_value = next(iter(cdi_yearly_entry.values()))

                    if not self._cdi_has_been_processed(date_obj):
                        self._save_raw(value, "monthly_cdi", date_obj)
                        self._save_raw(yearly_value, "yearly_cdi", date_obj)
                        cdi_dict = self._transform_cdi(value, yearly_value, date_obj)
                        self._load_cdi_to_excel(cdi_dict)
        except Exception as e:
            print(f"Erro ao processar dados de CDI, encerrando passo CDI. Exception: {e}")

        print("> Processando e salvando dados (IPCA)...")
        try:
            for ipca_entry in ipca_data:
                for date_str, value in ipca_entry.items():
                    date_obj = datetime.strptime(date_str, API_DATE_FORMAT)

                    if not self._ipca_has_been_processed(date_obj):
                        self._save_raw(value / 100, "ipca", date_obj)
                        ipca_dict = self._transform_ipca(value / 100, date_obj)
                        self._load_ipca_to_excel(ipca_dict)
        except Exception as e:
            print(f"Erro ao processar dados de IPCA, encerrando passo IPCA. Exception: {e}")


    def _run_backfill(self):
        cdi_raw_dir = pr_root / "data" / "raw" / "cdi"
        ipca_raw_dir = pr_root / "data" / "raw" / "ipca"

        if not cdi_raw_dir.exists() or not ipca_raw_dir.exists():
            print("Nenhum dado bruto encontrado.")
            return

        cdi_processed_dates = set()
        for file in cdi_raw_dir.glob("*.json"):
            cdi_parts = file.stem.split("_")[1].split("-")
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

        cdi_data = yearly_cdi = []
        ipca_data = []

        try:
            cdi_data, yearly_cdi = self._fetch_cdi(cdi_min_date, cdi_max_date)
        except Exception as e:
            print(f"Erro ao buscar dados de CDI: {e}")
            cdi_data, yearly_cdi = [], []

        try:
            ipca_data = self._fetch_ipca(ipca_min_date, ipca_max_date)
        except Exception as e:
            print(f"Erro ao buscar dados de IPCA: {e}")
            ipca_data = []

        print("> Processando e salvando dados (CDI)...")
        try:
            for cdi_entry, cdi_yearly_entry in zip(cdi_data, yearly_cdi):
                for date_str, value in cdi_entry.items():
                    date_obj = datetime.strptime(date_str, API_DATE_FORMAT)
                    yearly_value = next(iter(cdi_yearly_entry.values()))

                    if is_business_day(date_obj) and date_obj not in cdi_processed_dates:
                        self._save_raw(value, "monthly_cdi", date_obj)
                        self._save_raw(yearly_value, "yearly_cdi", date_obj)
                        cdi_dict = self._transform_cdi(value, yearly_value, date_obj)
                        self._load_cdi_to_excel(cdi_dict)
                        filled_count += 1
        except Exception as e:
            print(f"Erro ao processar/salvar CDI: {e}")

        print("> Processando e salvando dados (IPCA)...")
        try:
            for ipca_entry in ipca_data:
                for date_str, value in ipca_entry.items():
                    date_obj = datetime.strptime(date_str, API_DATE_FORMAT)
                    month_start = datetime(date_obj.year, date_obj.month, 1)

                    if month_start not in ipca_processed_dates:
                        val_dec = value / 100 if isinstance(value, (int, float)) else value
                        self._save_raw(val_dec, "ipca", date_obj)
                        ipca_dict = self._transform_ipca(val_dec, date_obj)
                        self._load_ipca_to_excel(ipca_dict)
                        filled_count += 1
        except Exception as e:
            print(f"Erro ao processar/salvar IPCA: {e}")

        print(f"Total de datas preenchidas: {filled_count}")







    # ============================
    #  PREPARE
    # ============================
    @staticmethod
    def _cdi_has_been_processed(dt: datetime) -> bool:
        """Define se o CDI já foi processado para a data fornecida."""
        filepath = pr_root / "data" / "raw" / "cdi" / f"cdi_{dt.strftime("%Y-%m")}.json"
        return filepath.exists()

    @staticmethod
    def _ipca_has_been_processed(dt: datetime) -> bool:
        """Define se o IPCA já foi processado para a data fornecida."""
        filepath = pr_root / "data" / "raw" / "ipca" / f"ipca_{dt.strftime("%Y-%m")}.json"
        return filepath.exists()

    # ============================
    #  FETCH
    # ============================

    @staticmethod
    def _fetch_date() -> datetime:
        """Obtém a data atual para execução da Pipeline."""
        return date_info()

    @staticmethod
    def _fetch_cdi(start_dt: datetime, end_dt: datetime = None) -> tuple[fetchReturns, fetchReturns]:
        """Obtém a taxa CDI mensal e anual para a data fornecida."""
        return get_monthly_cdi_rate(start_dt, end_dt), get_yearly_cdi_rate(start_dt, end_dt)


    @staticmethod
    def _fetch_ipca(start_dt: datetime, end_dt: datetime = None) -> fetchReturns:
        """Obtém a taxa IPCA mensal para a data fornecida."""
        return get_monthly_ipca(start_dt, end_dt)


    @staticmethod
    def _save_raw(data: float, name: str, dt: datetime) -> str:
        """Salva os dados brutos obtidos em um arquivo JSON."""
        folder = pr_root / "data" / "raw" / name
        folder.mkdir(parents=True, exist_ok=True)

        filepath = folder / f"{name}_{dt.strftime("%Y-%m")}.json"

        payload = {
            "reference_date": f"{dt.strftime("%Y-%m")}",
            "type": name,
            "value": data
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        return str(filepath)

    # ============================
    #  TRANSFORM
    # ============================

    @staticmethod
    def _transform_cdi(cdi_monthly_rate: float, cdi_annual_rate: float, dt: datetime) -> dict[str, float | int]:
        """Transforma os dados brutos de CDI em um dicionário estruturado para o load."""
        return {"year": dt.year, "month": dt.month, "cdi_annual_rate": cdi_annual_rate, "cdi_monthly_rate": cdi_monthly_rate}


    @staticmethod
    def _transform_ipca(ipca_monthly_rate: float, dt: datetime) -> dict[str, float | int]:
        """Transforma os dados brutos de IPCA em um dicionário estruturado para o load."""
        return {"year": dt.year, "month": dt.month, "ipca_monthly_rate": ipca_monthly_rate}

    # ============================
    #  LOAD
    # ============================

    # Desabilitado por enquanto para encaixar melhor com os loaders específicos para cada dado
    # def _load(self, new_row):
    #     self.loaders[self.persistence_mode](new_row)
    #     return

    @staticmethod
    def _load_cdi_to_excel(new_row: dict[str, float | int]):
        """Carrega os dados de CDI para o Excel."""
        register_cdi_data(new_row)


    @staticmethod
    def _load_ipca_to_excel(new_row: dict[str, float | int]):
        """Carrega os dados de IPCA para o Excel."""
        register_ipca_data(new_row)
