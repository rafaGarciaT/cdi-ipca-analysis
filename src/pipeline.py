from datetime import datetime

from src.indicators.base import BaseIndicator
from src.indicators.cdi_indicator import CDIIndicator
from src.indicators.ipca_indicator import IPCAIndicator
from src.storage import RawStorageFactory, ProcessedStorageFactory, cdi_schema, ipca_schema
from src.utils.date_utils import date_info
from src.config import pr_root, BCB_API_DATE_FORMAT
from src.utils.logger import Logger


class Pipeline:
    """Orquestrador principal da pipeline de coleta e processamento de indicadores econômicos.
    Coordena a coleta de dados, transformação e armazenamento.

    Attributes:
        target_year (int, optional): Ano alvo para processamento.
        indicators (list): Lista de instâncias de indicadores a serem processados.
        logger (Logger): Instância do logger para rastreamento de execução.

    Examples:
        >>> pipeline_yearly = Pipeline(
        ...     execution_mode='yearly',
        ...     target_year=2024,
        ...     processed_persistence_mode='excel'
        ... )
        >>> pipeline_yearly.run()
    """
    def __init__(self, raw_persistence_mode: str = "json",
                 processed_persistence_mode: str = "excel",
                 execution_mode: str = "month",
                 target_year: int = None):
        """Inicializa a pipeline com os modos de persistência e execução especificados.

        Args:
            raw_persistence_mode (str): Modo de persistência para dados brutos ('json', 'csv', etc.).
            processed_persistence_mode (str): Modo de persistência para dados processados ('excel', 'csv', etc.).
            execution_mode (str): Modo de execução ('month', 'yearly', 'backfill').
            target_year (int, optional): Ano alvo para processamento (usado apenas no modo 'yearly').
        """
        self.execution_mode = execution_mode
        self.target_year = target_year or datetime.now().year
        self.indicators = self._setup_indicators(raw_persistence_mode, processed_persistence_mode)
        self.logger = Logger("pipeline")


    @staticmethod
    def _setup_indicators(raw_mode: str, processed_mode: str):
        """Configura os indicadores com os modos de persistência especificados. Chamado durante a inicialização da Pipeline.

        Args:
            raw_mode (str): Modo de persistência para dados brutos ('json', 'csv', etc.).
            processed_mode (str): Modo de persistência para dados processados ('excel', 'csv', etc.).

        Returns:
            list: Lista de instâncias de indicadores configurados.
        """
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
        """Executa a pipeline a partir de uma configuração."""
        self.logger.info(f"INICIANDO PIPELINE | Modo: {self.execution_mode}" + (f" | Ano alvo: {self.target_year}" if self.execution_mode == "yearly" else ""))

        dt = date_info()

        if self.execution_mode == "month":
            self._run_month(dt)
        elif self.execution_mode == "yearly":
            self._run_year(dt)
        elif self.execution_mode == "backfill":
            self._run_backfill()
        else:
            self.logger.error(f"Modo desconhecido: {self.execution_mode}")

        self.logger.info("FINALIZANDO PIPELINE")

    def _run_month(self, dt: datetime):
        """Processa os indicadores para o mês atual, verificando se já foram processados para a data atual.

        Args:
            dt(datetime): Data atual para verificação e processamento dos indicadores.
        """
        for indicator in self.indicators:
            self._process_indicator_for_date(indicator, dt)

    def _process_indicator_for_date(self, indicator: BaseIndicator, dt: datetime):
        """Função auxiliar para processar um indicador específico para uma data específica.

        Args:
            indicator(BaseIndicator): Instância do indicador a ser processado.
            dt(datetime): Data para a qual o indicador deve ser processado.
        """
        self.logger.info(f"{indicator.name} | Buscando, processando e armazenando dados")

        if indicator.has_been_processed(dt):
            self.logger.warning(f"{indicator.name} já foi processado nessa data.")
            return

        try:
            data_list = indicator.fetch(dt)
            date_str, raw_data = data_list[0]
            indicator.save_raw(raw_data, dt)
            processed_data = indicator.transform(raw_data, dt)
            indicator.load_processed(processed_data)
        except Exception as e:
            self.logger.error(f"Erro ao processar {indicator.name}: {e}")

    def _run_year(self, dt: datetime):
        """Processa os indicadores para um ano em específico.

        Args:
            dt(datetime): Data atual. Necessária para limitar o processamento caso o ano alvo seja o ano atual.
        """
        start_date = datetime(self.target_year, 1, 1)
        end_date = min(datetime(self.target_year, 12, 31), dt)

        for indicator in self.indicators:
            self._process_indicator_for_period(indicator, start_date, end_date)

    def _process_indicator_for_period(self, indicator: BaseIndicator, start_dt: datetime, end_dt: datetime):
        """Função auxiliar para processar um indicador específico para um período definido por uma data de início e uma data final.

        Args:
            indicator(BaseIndicator): Instância do indicador a ser processado.
            start_dt(datetime): Data de início para verificação e processamento dos indicadores.
            end_dt(datetime): Data final para verificação e processamento dos indicadores.
        """
        self.logger.info(f"{indicator.name} | Buscando, processando e armazenando dados")

        try:
            data_list = indicator.fetch(start_dt, end_dt)

            for date_str, raw_data in data_list:
                date_obj = datetime.strptime(date_str, BCB_API_DATE_FORMAT)

                if not indicator.has_been_processed(date_obj):
                    indicator.save_raw(raw_data, date_obj)
                    processed = indicator.transform(raw_data, date_obj)
                    indicator.load_processed(processed)
        except Exception as e:
            self.logger.error(f"Erro ao processar {indicator.name}: {e}")

    def _run_backfill(self):
        """Preenche lacunas de dados processados para os indicadores, buscando as datas já processadas e preenchendo os períodos faltantes."""
        for indicator in self.indicators:
            self._backfill_indicator(indicator)

    def _backfill_indicator(self, indicator: BaseIndicator):
        """Função auxiliar para encontrar as lacunas de dados processados para um indicador específico e preenchê-las.

        Args:
            indicator(BaseIndicator): Instância do indicador a ser processado.
        """
        self.logger.info(f"{indicator.name} | Buscando, processando e armazenando dados")

        processed_dates = indicator.raw_storage.get_collected_values(indicator.raw_storage.base_path)

        if not processed_dates:
            self.logger.warning(f"Dados insuficientes para backfill de {indicator.name}.")
            return

        min_date = min(processed_dates)
        max_date = max(processed_dates)

        self.logger.info(f"Preenchendo lacunas entre {min_date.date()} e {max_date.date()}...")

        self._process_indicator_for_period(indicator, min_date, max_date)
