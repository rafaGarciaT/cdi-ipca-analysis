from src.config import BCB_API_DATE_FORMAT
from src.indicators.base_indicator import BaseIndicator
from src.fetch import get_monthly_ipca
from src.transform.base_transform import calc_accumulated_ytd_rate
from datetime import datetime


class IPCAIndicator(BaseIndicator):
    def __init__(self, raw_storage, processed_storage):
        super().__init__("IPCA", raw_storage, processed_storage)

    def fetch(self, start_dt: datetime, end_dt: datetime = None):
        data = get_monthly_ipca(start_dt, end_dt)
        # API pode retornar um único valor ou uma lista, normalizamos aqui
        if isinstance(data, list):
            result = []
            for entry in data:
                date_str = list(entry.keys())[0]
                result.append((date_str, entry[date_str]))
            return result
        else:
            date_str = start_dt.strftime(BCB_API_DATE_FORMAT)
            return [(date_str, data)]

    def transform(self, raw_data: float, dt: datetime) -> dict:
        monthly_rate = raw_data / 100

        monthly_rates_ytd = self.raw_storage.get_values_until(str(dt.year), dt.strftime("%Y-%m"))

        all_rates = monthly_rates_ytd
        if len(monthly_rates_ytd) < 12:
            prev_year_rates = self.raw_storage.get_values_until(str(dt.year - 1), f"{dt.year - 1}-12")
            all_rates = (prev_year_rates + monthly_rates_ytd)[-12:]

        last_12m = all_rates if len(all_rates) == 12 else None
        ytd_rate = calc_accumulated_ytd_rate(monthly_rates_ytd)
        rate_12m = calc_accumulated_ytd_rate(last_12m) if last_12m else float('nan')

        return {
            "date": dt.strftime("%Y-%m"),
            "ipca_monthly_rate": monthly_rate,
            "ipca_accumulated_ytd_rate": ytd_rate,
            "ipca_12m_rate": rate_12m
        }

    def save_raw(self, data: float, dt: datetime):
        super().save_raw(round(data / 100, 6), dt)
