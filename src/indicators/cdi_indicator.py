from src.config import BCB_API_DATE_FORMAT
from src.indicators.base_indicator import BaseIndicator
from src.fetch import get_monthly_cdi_rate, get_yearly_cdi_rate
from src.transform.base_transform import calc_accumulated_ytd_rate
from datetime import datetime


class CDIIndicator(BaseIndicator):
    def __init__(self, raw_storage, processed_storage):
        super().__init__("CDI", raw_storage, processed_storage)

    def fetch(self, start_dt: datetime, end_dt: datetime = None) -> list:
        monthly = get_monthly_cdi_rate(start_dt, end_dt)
        yearly = get_yearly_cdi_rate(start_dt, end_dt)
        # API pode retornar um único valor ou uma lista, normalizamos aqui
        if isinstance(monthly, list):
            result = []
            for m_dict, y_dict in zip(monthly, yearly):
                date_str = list(m_dict.keys())[0]
                result.append((date_str, (m_dict[date_str], y_dict[date_str])))
            return result
        else:
            date_str = start_dt.strftime(BCB_API_DATE_FORMAT)
            return [(date_str, (monthly, yearly))]

    def transform(self, raw_data: tuple, dt: datetime) -> dict:
        monthly_rate, yearly_rate = raw_data
        monthly_rate = monthly_rate / 100
        yearly_rate = yearly_rate / 100

        monthly_rates_ytd = self.raw_storage.get_values_until(str(dt.year), dt.strftime("%Y-%m"))
        monthly_rates_ytd = [v["monthly"] if isinstance(v, dict) else v for v in monthly_rates_ytd]

        all_rates = monthly_rates_ytd
        if len(monthly_rates_ytd) < 12:
            prev_year_rates = self.raw_storage.get_values_until(str(dt.year - 1), f"{dt.year - 1}-12")
            prev_year_rates = [v["monthly"] if isinstance(v, dict) else v for v in prev_year_rates]
            all_rates = (prev_year_rates + monthly_rates_ytd)[-12:]

        last_12m = all_rates if len(all_rates) == 12 else None
        ytd_rate = calc_accumulated_ytd_rate(monthly_rates_ytd)
        rate_12m = calc_accumulated_ytd_rate(last_12m) if last_12m else float('nan')

        return {
            "date": dt.strftime("%Y-%m"),
            "cdi_annual_rate": yearly_rate,
            "cdi_monthly_rate": monthly_rate,
            "cdi_accumulated_ytd_rate": ytd_rate,
            "cdi_12m_rate": rate_12m
        }

    def save_raw(self, data: tuple, dt: datetime):
        monthly, yearly = data
        combined_data = {
            "monthly": round(monthly / 100, 6),
            "yearly": round(yearly / 100, 6)
        }
        self.raw_storage.save(combined_data, dt.strftime("%Y-%m"))