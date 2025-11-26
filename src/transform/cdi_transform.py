def calc_cdi_anual(cdi_diario: float) -> float:
    return round(((1 + cdi_diario / 100) ** 252 - 1) * 100, 2)