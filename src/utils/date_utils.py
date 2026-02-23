from datetime import datetime
from pandas import bdate_range


def date_info() -> datetime:
    """Retorna um objeto datetime com a data e hora atuais.

    Returns:
        datetime: Data e hora atuais.
    """
    return datetime.now()


def is_business_day(date: datetime) -> bool:
    """Verifica se uma data é um dia útil. Não utilizado atualmente.

    Args:
        date (datetime): Data a ser verificada.

    Returns:
        bool: True se a data for um dia útil, False caso contrário.
    """
    return bool(len(bdate_range(date, date)))
