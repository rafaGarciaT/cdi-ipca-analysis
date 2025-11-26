import pandas as pd

def calc_ipca_acumulado(valores: list[float]) -> float:
    serie = pd.Series(valores)
    return (1 + serie / 100).prod() - 1