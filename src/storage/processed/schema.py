import pandas as pd


def cdi_schema() -> pd.DataFrame:
    df = pd.DataFrame({
        "date": [],
        "cdi_annual_rate": [],
        "cdi_monthly_rate": [],
    })
    return df


def ipca_schema() -> pd.DataFrame:
    df = pd.DataFrame({
        "date": [],
        "ipca_monthly_rate": [],
    })
    return df
