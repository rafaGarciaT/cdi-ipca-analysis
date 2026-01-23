from pathlib import Path

# Diretório raiz do projeto
pr_root = Path(__file__).parent.parent

# Links das APIs utilizadas
API_BASE_URL_CDI_INTERESTS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados"
API_BASE_URL_CDI_YEARLY = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4392/dados"
API_BASE_URL_CDI_MONTHLY = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4391/dados"
API_BASE_URL_IPCA_MONTHLY = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados"

# Formato de data utilizado nas requisições à API do Banco Central do Brasil
BCB_API_DATE_FORMAT = "%d/%m/%Y"
