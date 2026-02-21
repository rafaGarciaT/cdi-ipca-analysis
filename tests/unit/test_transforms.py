import pytest
from src.transform.base_transform import calc_accumulated_ytd_rate


class TestCalcAccumulatedYtdRate:
    """Testes para cálculo de taxa acumulada."""

    def test_empty_list(self):
        """Taxa acumulada de lista vazia deve ser 0.0."""
        result = calc_accumulated_ytd_rate([])
        assert result == 0.0

    def test_single_rate(self):
        """Taxa acumulada de um único mês deve ser a própria taxa."""
        result = calc_accumulated_ytd_rate([0.01])
        assert round(result, 6) == 0.01

    def test_multiple_positive_rates(self):
        """Múltiplas taxas positivas devem compor corretamente."""
        rates = [0.01, 0.02, 0.015]
        result = calc_accumulated_ytd_rate(rates)
        expected = (1.01 * 1.02 * 1.015) - 1
        assert abs(result - expected) < 1e-10

    def test_with_negative_rate(self):
        """Deve lidar com taxas negativas."""
        rates = [0.01, -0.005, 0.02]
        result = calc_accumulated_ytd_rate(rates)
        expected = (1.01 * 0.995 * 1.02) - 1
        assert abs(result - expected) < 1e-10

    def test_zero_rate(self):
        """Deve lidar com taxa zero."""
        rates = [0.01, 0.0, 0.02]
        result = calc_accumulated_ytd_rate(rates)
        expected = (1.01 * 1.0 * 1.02) - 1
        assert abs(result - expected) < 1e-10

    @pytest.mark.parametrize("rates,expected", [
        ([0.005], 0.005),
        ([0.005, 0.005], 0.010025),
        ([0.01] * 12, 0.126825030131969),  # ~12.68% ao ano
    ])
    def test_parametrized_scenarios(self, rates, expected):
        """Testa múltiplos cenários via parametrização."""
        result = calc_accumulated_ytd_rate(rates)
        assert abs(result - expected) < 1e-10