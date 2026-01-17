from datetime import datetime
from pandas import bdate_range


def date_info() -> datetime:
    """Retorna um objeto datetime com a data e hora atuais."""
    return datetime.now()


def is_business_day(date: datetime) -> bool:
    """Verifica se uma data é um dia útil."""
    return bool(len(bdate_range(date, date)))
