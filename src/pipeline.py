from datetime import datetime
from src.indicators.cdi_indicator import CDIIndicator
from src.indicators.ipca_indicator import IPCAIndicator
from src.storage import RawStorageFactory, ProcessedStorageFactory, cdi_schema, ipca_schema
from src.utils.date_utils import date_info, is_business_day
from src.config import pr_root, BCB_API_DATE_FORMAT


class Pipeline:
    def __init__(self, raw_persistence_mode: str = "json",
                 processed_persistence_mode: str = "excel",
                 execution_mode: str = "month",
                 target_year: int = None):
        self.execution_mode = execution_mode
        self.target_year = target_year or datetime.now().year
        self.indicators = self._setup_indicators(raw_persistence_mode, processed_persistence_mode)


    def _setup_indicators(self, raw_mode: str, processed_mode: str):
        ext = "xlsx" if processed_mode == "excel" else "csv"

        cdi_indicator = CDIIndicator(
            raw_storage=RawStorageFactory.create_storage(raw_mode, "cdi"),
            processed_storage=ProcessedStorageFactory.create_storage(
                processed_mode,
                pr_root / "data" / "processed" / f"cdi_data.{ext}",
                cdi_schema
            )
        )

        ipca_indicator = IPCAIndicator(
            raw_storage=RawStorageFactory.create_storage(raw_mode, "ipca"),
            processed_storage=ProcessedStorageFactory.create_storage(
                processed_mode,
                pr_root / "data" / "processed" / f"ipca_data.{ext}",
                ipca_schema
            )
        )

        return [cdi_indicator, ipca_indicator]

    def run(self):
        print("=== INICIANDO PIPELINE ===")
        print(f"Modo de execução: {self.execution_mode}\n> Preparando...")

        dt = date_info()

        if self.execution_mode == "month":
            self._run_month(dt)
        elif self.execution_mode == "yearly":
            self._run_year(dt)
        elif self.execution_mode == "backfill":
            self._run_backfill()
        else:
            print(f"Modo desconhecido: {self.execution_mode}")

        print("=== PIPELINE FINALIZADA ===")

    def _run_month(self, dt: datetime):
        if not is_business_day(dt):
            print("Data informada não é um dia útil. Encerrando pipeline.")
            return

        for indicator in self.indicators:
            self._process_indicator_for_date(indicator, dt)

    def _process_indicator_for_date(self, indicator, dt: datetime):
        print(f"\n> {indicator.name}\nBuscando dados...")

        if indicator.has_been_processed(dt):
            print(f"{indicator.name} já foi processado nessa data.")
            return

        try:
            data_list = indicator.fetch(dt)
            print("Processando e salvando dados...")

            date_str, raw_data = data_list[0]
            indicator.save_raw(raw_data, dt)
            processed_data = indicator.transform(raw_data, dt)
            indicator.load_processed(processed_data)
        except Exception as e:
            print(f"Erro ao processar {indicator.name}: {e}")

    def _run_year(self, dt: datetime):
        print(f"> Recolhendo dados do ano {self.target_year}...\n")

        start_date = datetime(self.target_year, 1, 1)
        end_date = min(datetime(self.target_year, 12, 31), dt)

        for indicator in self.indicators:
            self._process_indicator_for_period(indicator, start_date, end_date)

    def _process_indicator_for_period(self, indicator, start_dt: datetime, end_dt: datetime):
        print(f"\n> Processando {indicator.name}...")

        try:
            data_list = indicator.fetch(start_dt, end_dt)

            for date_str, raw_data in data_list:
                date_obj = datetime.strptime(date_str, BCB_API_DATE_FORMAT)

                if not indicator.has_been_processed(date_obj):
                    indicator.save_raw(raw_data, date_obj)
                    processed = indicator.transform(raw_data, date_obj)
                    indicator.load_processed(processed)
        except Exception as e:
            print(f"Erro ao processar {indicator.name}: {e}")

    def _run_backfill(self):
        print("> Iniciando backfill...")

        for indicator in self.indicators:
            self._backfill_indicator(indicator)

    def _backfill_indicator(self, indicator):
        print(f"\n> Backfill para {indicator.name}...")

        processed_dates = indicator.raw_storage.get_collected_values(indicator.raw_storage.base_path)

        if not processed_dates:
            print(f"Dados insuficientes para backfill de {indicator.name}.")
            return

        min_date = min(processed_dates)
        max_date = max(processed_dates)

        print(f"Preenchendo lacunas entre {min_date.date()} e {max_date.date()}...")

        self._process_indicator_for_period(indicator, min_date, max_date)
