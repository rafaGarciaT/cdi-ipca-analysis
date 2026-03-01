from math import sqrt
from typing import Iterable, List


def _validate(data: Iterable[float]) -> Iterable[float]:
    """Valida os dados de entrada, garantindo que sejam uma lista de números e não vazia."""
    values = list(data)
    if len(values) == 0:
        raise ValueError("Lista deve conter pelo menos um número.")
    return values

# =============================================
# Tendência central
# =============================================

def mean(data: Iterable[float]) -> float:
    """Devolve a média aritmética. Estimador da média populacional."""
    values = _validate(data)
    return sum(values) / len(values)


def median(data: Iterable[float]) -> float:
   """Devolve a mediana. Valor que separa a amostra em duas partes iguais."""
   values = sorted(_validate(data))
   return _median_even(values) if len(values) % 2 == 0 else _median_odd(values)


def _median_odd(data: list[float]) -> float:
    """Devolve a mediana no caso de uma lista com número ímpar de elementos."""
    return data[len(data) // 2]  # Número do meio da lista ordenada


def _median_even(data: list[float]) -> float:
    """Devolve a mediana no caso de uma lista com número par de elementos."""
    mid = len(data) // 2
    return (data[mid - 1] + data[mid]) / 2  # Média dos dois números do meio da lista ordenada

# =============================================
# Quantis
# =============================================

def quantile(data: Iterable[float], p: float) -> float:
    """Devolve o quantil amostral com interpolação linear."""
    if not 0 <= p <= 1:
        raise ValueError("p precisa estar entre 0 e 1.")

    values = sorted(_validate(data))
    n = len(values)

    index = p * (n - 1)
    lower = int(index)
    upper = lower + 1

    if upper >= n:
        return values[lower]

    weight = index - lower
    return values[lower] * (1 - weight) + values[upper] * weight

# =============================================
# Dispersão
# =============================================

def de_mean(data: Iterable[float]) -> list[float]:
    """Devolve desvios da média. A lista de dados com a média subtraída de cada valor."""
    data_mean = mean(data)
    return [x - data_mean for x in data]


def variance(data: Iterable[float]) -> float:
    """Devolve a variância de uma lista de números com a correção de Bessel."""
    values = _validate(data)
    n = len(values)

    if n < 2:
        raise ValueError("Variância requer pelo menos dois elementos.")

    deviations = de_mean(values)
    return sum(d ** 2 for d in deviations) / (n - 1)


def standard_deviation(data: Iterable[float]) -> float:
    """Devolve o desvio padrão de uma lista de números."""
    return sqrt(variance(data))

def interquartile_range(data: Iterable[float]) -> float:
    """Devolve a amplitude interquartil de uma lista de números."""
    return quantile(data, 0.75) - quantile(data, 0.25)

def coefficient_of_variation(data: Iterable[float]) -> float:
    """Devolve o coeficiente de variação de uma lista de números.
    A razão entre o desvio padrão e a média, expressando a dispersão relativa dos dados em relação à média.
    """
    values = _validate(data)
    x_bar = mean(values)
    if x_bar == 0:
        raise ValueError("Mean is zero; coefficient of variation undefined.")
    return standard_deviation(values) / x_bar


# =========================
# Assimetria e Curtose
# =========================

def skewness(data: Iterable[float]) -> float:
    """Devolve assimetria amostral corrigida (Fisher-Pearson).
    Valor referente ao formato da distribuição.
    Se pende para a direita (return positive) ou para a esquerda (return negativo), ou se é simétrica (return zero).
    """
    values = _validate(data)
    n = len(values)

    if n < 3:
        raise ValueError("Assimetria requer pelo menos três pontos de dados.")

    mean_ = mean(values)
    std_ = standard_deviation(values)

    if std_ == 0:
        return 0.0

    normalized = [(x - mean_) / std_ for x in values]
    return (n / ((n - 1) * (n - 2))) * sum(z ** 3 for z in normalized)


def kurtosis(data: Iterable[float]) -> float:
    """Devolve curtose amostral corrigida (excesso de curtose).
    Valor referente ao formato da distribuição.
    Se a distribuição é mais achatada (return negative) ou mais pontuda (return positive) do que a distribuição normal, ou se tem a mesma curtose (return zero).
    """
    values = _validate(data)
    n = len(values)

    if n < 4:
        raise ValueError("Kurtosis requires at least four data points.")

    mean_ = mean(values)
    std_ = standard_deviation(values)

    if std_ == 0:
        return -3.0

    normalized = [(x - mean_) / std_ for x in values]

    term1 = (n * (n + 1)) / ((n - 1) * (n - 2) * (n - 3))
    term2 = sum(z ** 4 for z in normalized)
    term3 = (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))

    return term1 * term2 - term3


# =========================
# Summary
# =========================

def summary(data: Iterable[float]) -> dict:
    """Devolve resumo estatístico completo."""
    values = _validate(data)

    return {
        "mean": mean(values),
        "median": median(values),
        "variance": variance(values),
        "std_dev": standard_deviation(values),
        "iqr": interquartile_range(values),
        "cv": coefficient_of_variation(values),
        "skewness": skewness(values),
        "kurtosis": kurtosis(values),
        "min": min(values),
        "max": max(values),
        "n": len(values),
    }