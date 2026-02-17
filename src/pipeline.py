from datetime import datetime
from src.fetch import get_monthly_cdi_rate, get_yearly_cdi_rate, get_monthly_ipca
from src.storage import RawStorageFactory, ProcessedStorageFactory, cdi_schema, ipca_schema, JsonRawStorage, \
    BaseRawStorage
from src.utils.date_utils import date_info, is_business_day
from src.config import pr_root, BCB_API_DATE_FORMAT

from typing import TypeAlias

fetchReturns: TypeAlias = float | list[dict[str, float]]

class Pipeline:
    def __init__(self, raw_persistence_mode: str = "json", processed_persistence_mode: str = "excel", execution_mode: str = "month", target_year: int = None):
        self.raw_persistence_mode = raw_persistence_mode
        self.processed_persistence_mode = processed_persistence_mode
        self.execution_mode = execution_mode
        self.target_year = target_year if target_year else datetime.now().year

        cdi_ext = "xlsx" if processed_persistence_mode == "excel" else "csv"
        ipca_ext = "xlsx" if processed_persistence_mode == "excel" else "csv"

        self.raw_monthly_cdi_storage = RawStorageFactory.create_storage(
            raw_persistence_mode,
            "monthly_cdi"
        )

        self.raw_yearly_cdi_storage = RawStorageFactory.create_storage(
            raw_persistence_mode,
            "yearly_cdi"
        )

        self.raw_ipca_storage = RawStorageFactory.create_storage(
            raw_persistence_mode,
            "ipca"
        )

        self.processed_cdi_storage = ProcessedStorageFactory.create_storage(
            processed_persistence_mode,
            pr_root / "data" / "processed" / f"cdi_data.{cdi_ext}",
            cdi_schema
        )

        self.processed_ipca_storage = ProcessedStorageFactory.create_storage(
            processed_persistence_mode,
            pr_root / "data" / "processed" / f"ipca_data.{ipca_ext}",
            ipca_schema
        )

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
                    # A API retorna o valor em porcentagem, então dividimos por 100 para obter o valor decimal
                    monthly_cdi = monthly_cdi / 100
                    yearly_cdi = yearly_cdi / 100
                    self._save_raw(monthly_cdi, dt, self.raw_monthly_cdi_storage)
                    self._save_raw(yearly_cdi, dt, self.raw_yearly_cdi_storage)
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
                    # A API retorna o valor em porcentagem, então dividimos por 100 para obter o valor decimal
                    monthly_ipca = monthly_ipca / 100
                    self._save_raw(monthly_ipca, dt, self.raw_ipca_storage)
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
                    date_obj = datetime.strptime(date_str, BCB_API_DATE_FORMAT)
                    yearly_value = next(iter(cdi_yearly_entry.values()))

                    if not self._cdi_has_been_processed(date_obj):
                        # A API retorna o valor em porcentagem, então dividimos por 100 para obter o valor decimal
                        value = value / 100
                        yearly_value = yearly_value / 100
                        self._save_raw(value, date_obj, self.raw_monthly_cdi_storage)
                        self._save_raw(yearly_value, date_obj, self.raw_yearly_cdi_storage)
                        cdi_dict = self._transform_cdi(value, yearly_value, date_obj)
                        self._load_cdi_to_excel(cdi_dict)
        except Exception as e:
            print(f"Erro ao processar dados de CDI, encerrando passo CDI. Exception: {e}")

        print("> Processando e salvando dados (IPCA)...")
        try:
            for ipca_entry in ipca_data:
                for date_str, value in ipca_entry.items():
                    date_obj = datetime.strptime(date_str, BCB_API_DATE_FORMAT)

                    if not self._ipca_has_been_processed(date_obj):
                        # A API retorna o valor em porcentagem, então dividimos por 100 para obter o valor decimal
                        value = value / 100
                        self._save_raw(value, date_obj, self.raw_ipca_storage)
                        ipca_dict = self._transform_ipca(value, date_obj)
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
                    date_obj = datetime.strptime(date_str, BCB_API_DATE_FORMAT)
                    yearly_value = next(iter(cdi_yearly_entry.values()))

                    if is_business_day(date_obj) and date_obj not in cdi_processed_dates:
                        # A API retorna o valor em porcentagem, então dividimos por 100 para obter o valor decimal
                        value = value / 100
                        yearly_value = yearly_value / 100
                        self._save_raw(value, date_obj, self.raw_monthly_cdi_storage)
                        self._save_raw(yearly_value, date_obj, self.raw_yearly_cdi_storage)
                        cdi_dict = self._transform_cdi(value, yearly_value, date_obj)
                        self._load_cdi_to_excel(cdi_dict)
                        filled_count += 1
        except Exception as e:
            print(f"Erro ao processar/salvar CDI: {e}")

        print("> Processando e salvando dados (IPCA)...")
        try:
            for ipca_entry in ipca_data:
                for date_str, value in ipca_entry.items():
                    date_obj = datetime.strptime(date_str, BCB_API_DATE_FORMAT)
                    month_start = datetime(date_obj.year, date_obj.month, 1)

                    if month_start not in ipca_processed_dates:
                        # A API retorna o valor em porcentagem, então dividimos por 100 para obter o valor decimal
                        value = value / 100
                        self._save_raw(value, date_obj, self.raw_ipca_storage)
                        ipca_dict = self._transform_ipca(value, date_obj)
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
    def _save_raw(data: float, dt: datetime, storage: BaseRawStorage) -> str:
        """Salva os dados brutos obtidos em um arquivo."""
        return storage.save(data, dt.strftime("%Y-%m"))

    # ============================
    #  TRANSFORM
    # ============================

    @staticmethod
    def _transform_cdi(cdi_monthly_rate: float, cdi_annual_rate: float, dt: datetime) -> dict[str, float | int]:
        """Transforma os dados brutos de CDI em um dicionário estruturado para o load."""
        return {"date": dt.strftime("%Y-%m"), "cdi_annual_rate": cdi_annual_rate, "cdi_monthly_rate": cdi_monthly_rate}


    @staticmethod
    def _transform_ipca(ipca_monthly_rate: float, dt: datetime) -> dict[str, float | int]:
        """Transforma os dados brutos de IPCA em um dicionário estruturado para o load."""
        return {"date": dt.strftime("%Y-%m"), "ipca_monthly_rate": ipca_monthly_rate}

    # ============================
    #  LOAD
    # ============================

    def _load_cdi_to_excel(self, new_row: dict[str, float | int]):
        """Carrega os dados de CDI para o Excel."""
        self.processed_cdi_storage.register_data(new_row)


    def _load_ipca_to_excel(self, new_row: dict[str, float | int]):
        """Carrega os dados de IPCA para o Excel."""
        self.processed_ipca_storage.register_data(new_row)
