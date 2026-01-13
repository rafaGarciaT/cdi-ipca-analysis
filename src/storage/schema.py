import pandas as pd


def cdi_schema() -> pd.DataFrame:
    df = pd.DataFrame({
        "year": [],
        "month": [],
        "cdi_annual_rate": [],
        # "cdi_daily_factor": [],
        "cdi_monthly_rate": [],
        # "cdi_accumulated": [],  # Acumulado no ano até a data
    })
    return df


def ipca_schema() -> pd.DataFrame:
    df = pd.DataFrame({
        "date": [],
        "ipca_monthly_rate": [],
        # "ipca_accumulated": [],  # Acumulado no ano até a data
    })
    return df