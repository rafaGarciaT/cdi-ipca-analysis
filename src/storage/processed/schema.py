import pandas as pd


def cdi_schema() -> pd.DataFrame:
    """Esquema para os dados processados do CDI.

    Returns:
        pd.DataFrame: DataFrame vazio com as colunas apropriadas para armazenar os dados processados do CDI.
    """
    df = pd.DataFrame({
        "date": [],
        "cdi_annual_rate": [],
        "cdi_monthly_rate": [],
        "cdi_accumulated_ytd_rate": [],
        "cdi_12m_rate": [],

    })
    return df


def ipca_schema() -> pd.DataFrame:
    """Esquema para os dados processados do IPCA.

    Returns:
        pd.DataFrame: DataFrame vazio com as colunas apropriadas para armazenar os dados processados do IPCA.
    """
    df = pd.DataFrame({
        "date": [],
        "ipca_monthly_rate": [],
        "ipca_accumulated_ytd_rate": [],
        "ipca_12m_rate": [],
    })
    return df
