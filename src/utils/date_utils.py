from datetime import datetime


def date_info():
    now = datetime.now()
    return {
        "d": now.day,
        "m": now.month,
        "a": now.year,
        "h": now.hour,
        "mn": now.minute,
        "s": now.second,
    }