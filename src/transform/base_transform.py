from typing import List

def calc_accumulated_ytd_rate(monthly_rates: List[float]) -> float:
    """Calcula o valor acumulado a partir de uma lista de taxas."""
    factor = 1.0
    for rate in monthly_rates:
        factor *= (1.0 + rate)
    return factor - 1.0
