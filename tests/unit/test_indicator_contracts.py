import pytest
import inspect
from datetime import datetime
from pathlib import Path
import importlib
from unittest.mock import Mock

from src.indicators.base_indicator import BaseIndicator
from src.storage.processed.excel_storage import ExcelProcessedStorage

# Dicionário de configuração para cada indicator
INDICATOR_TEST_DATA = {
    "CDI": {
        "raw_data": (1.0, 12.0),
        "monthly_rates_ytd": [0.01, 0.011, 0.009],
        "prev_year_rates": [0.008] * 12
    },
    "IPCA": {
        "raw_data": 0.5,
        "monthly_rates_ytd": [0.004, 0.005, 0.006],
        "prev_year_rates": [0.003] * 12
    }
}


class TestIndicatorContracts:
    """Testa contratos entre indicators e seus schemas automaticamente."""

    @pytest.fixture
    def all_indicator_classes(self):
        """Descobre automaticamente todas as classes que herdam de BaseIndicator."""
        indicators_path = Path("src/indicators")
        indicator_classes = []

        for file in indicators_path.glob("*_indicator.py"):
            if file.name == "base_indicator.py":
                continue

            module_name = f"src.indicators.{file.stem}"
            module = importlib.import_module(module_name)

            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, BaseIndicator) and
                        obj is not BaseIndicator and
                        obj.__module__ == module_name):
                    indicator_classes.append(obj)

        return indicator_classes

    def test_all_indicators_transform_matches_schema(self, tmp_path, all_indicator_classes):
        """Verifica que transform() de TODOS os indicators retorna dict compatível com schema."""
        schema_module = importlib.import_module("src.storage.processed.schema")

        for indicator_class in all_indicator_classes:
            # Descobre o schema correspondente
            schema_func_name = f"{indicator_class.__name__.replace('Indicator', '').lower()}_schema"

            if not hasattr(schema_module, schema_func_name):
                pytest.fail(f"Schema function '{schema_func_name}' não encontrada para {indicator_class.__name__}")

            schema_func = getattr(schema_module, schema_func_name)
            processed = ExcelProcessedStorage(tmp_path / f"{schema_func_name}.xlsx", schema_func)

            # Mock do raw_storage
            raw_storage_mock = Mock()

            indicator = indicator_class(raw_storage_mock, processed)

            try:
                dt = datetime(2024, 1, 15)

                # Busca configuração de teste
                test_config = INDICATOR_TEST_DATA.get(
                    indicator.name,
                    {
                        "raw_data": 0.5,
                        "monthly_rates_ytd": [0.005] * 3,
                        "prev_year_rates": [0.004] * 12
                    }
                )

                # Configura mock para retornar dados necessários
                raw_storage_mock.get_values_until.side_effect = [
                    test_config["monthly_rates_ytd"],  # Primeira chamada: YTD
                    test_config["prev_year_rates"]  # Segunda chamada: ano anterior
                ]

                # Executa transform
                result = indicator.transform(test_config["raw_data"], dt)

                # Busca schema
                schema_df = schema_func()

                assert isinstance(result, dict), \
                    f"{indicator_class.__name__}.transform() deve retornar dict, retornou {type(result)}"

                assert list(result.keys()) == schema_df.columns.tolist(), \
                    f"{indicator_class.__name__}: Colunas ou ordem diferente.\n" \
                    f"Esperado: {schema_df.columns.tolist()}\n" \
                    f"Retornado: {list(result.keys())}"

            except Exception as e:
                pytest.fail(f"{indicator_class.__name__} falhou no teste de contrato: {str(e)}")
