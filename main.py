from src.fetch.fetch_cdi import get_cdi
from src.fetch.fetch_ipca import get_ipca
from src.transform.cdi_transform import calc_cdi_anual
from src.transform.ipca_transform import calc_ipca_acumulado
from src.utils.date_utils import date_info

date = date_info()

# CDI
cdi_dia = get_cdi(date["d"], date["m"], date["a"])
cdi_ano = calc_cdi_anual(cdi_dia)

# IPCA
ipca_lista = get_ipca(date["d"], date["m"], date["a"])
ipca_acum = calc_ipca_acumulado([i["valor"] for i in ipca_lista])