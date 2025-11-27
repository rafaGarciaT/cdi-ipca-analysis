from src.fetch.fetch_cdi import get_cdi
from src.fetch.fetch_ipca import get_ipca


class Pipeline:
    def __init__(self, persistence_mode="excel"):
        self.persistence_mode = persistence_mode

        self.loaders = {
            "excel": self._load_to_excel,
            "sqlite": self._load_tosqlite
        }

    def run(self, day, month, year):
        print("=== INICIANDO PIPELINE ===>")

        print("> Buscando dados...") # -------- FETCH --------
        dados_cdi = self._fetch_cdi(day, month, year)
        dados_icpa = self._fetch_icpa(month, year)

        print("> Processando e calculando...") # -------- TRANSFORM --------
        rentabilidade = self._transform(dados_cdi)
        inflacao = self._transform(dados_icpa)

        print("> Salvando resultados...") # -------- LOAD --------
        self._load(rentabilidade)

        print("=== PIPELINE FINALIZADA ===")

    # ============================
    #  FETCH
    # ============================

    def _fetch_cdi(self, day, month, year):
        return get_cdi(day, month, year) # float

    def _fetch_icpa(self,month, year):
        return get_ipca(month, year) # float

    # ============================
    #  TRANSFORM
    # ============================

    def _transform(self, dados_cdi):
        # TODO: implementar transform
        return

    # ============================
    #  LOAD
    # ============================

    def _load(self, resultado):
        self.loaders[self.persistence_mode](resultado)
        return

    def _load_to_excel(self, resultado):
        # TODO: implementar persistência em excel
        return

    def _load_to_sqlite(self, resultado):
        # TODO: implementar persistência em sqlite
        return
