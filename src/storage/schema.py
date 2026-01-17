import pandas as pd


def cdi_schema() -> pd.DataFrame:
    df = pd.DataFrame({
        "year": [],
        "month": [],
        "cdi_annual_rate": [],
        "cdi_monthly_rate": [],
    })
    return df


def ipca_schema() -> pd.DataFrame:
    df = pd.DataFrame({
        "year": [],
        "month": [],
        "ipca_monthly_rate": [],
    })
    return df
