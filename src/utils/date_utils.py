from datetime import datetime
from pandas import bdate_range


def date_info():
    return datetime.now()

def is_business_day(date):
    return bool(len(bdate_range(date, date)))