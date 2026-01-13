from src.fetch.fetch_cdi import get_cdi
from src.fetch.fetch_ipca import get_monthly_ipca
from src.transform.cdi_transform import calc_accumulated_cdi
from src.utils.date_utils import date_info
from src.utils.directory_utils import clear_data_folders
from src.pipeline import Pipeline

date = date_info()

# CDI
# cdi_dia = get_cdi(date["d"], date["m"], date["a"])
# cdi_ano = calc_cdi_anual(cdi_dia)

# IPCA
# ipca_lista = get_ipca(date["d"], date["m"], date["a"])
# ipca_acum = calc_ipca_acumulado([i["valor"] for i in ipca_lista])
clear_data_folders()
pipeline = Pipeline("excel", "yearly", 2025)
pipeline.run()