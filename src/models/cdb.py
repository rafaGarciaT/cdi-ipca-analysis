from datetime import datetime
import numpy as np


class Cdb:
    def __init__(self, percentage, start_date, value):
        self.percentage = percentage
        self.start_date = start_date  # "YYYY-MM-DD" / "AAAA-MM-DD"
        self.value = value

    def business_days_count(self):
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        end_date = datetime.today().date()
        count = np.busday_count(start_date, end_date).astype(int)
        return int(count)

    def calendar_days_count(self):
        start_date = datetime.strptime(self.start_date, "%Y-%m-%d").date()
        end_date = datetime.today().date()
        return (end_date - start_date).days

