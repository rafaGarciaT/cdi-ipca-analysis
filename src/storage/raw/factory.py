from src.storage.raw.base import BaseRawStorage
from src.storage.raw.json_storage import JsonRawStorage


class RawStorageFactory:
    """Fábrica para criar instâncias de armazenamento de dados brutos.
    Deve ser chamado pelo indicador com a string de tipo de armazenamento e o tipo de dado correspondente.
    """
    @staticmethod
    def create_storage(storage_type: str, data_type: str) -> BaseRawStorage:
        """Cria uma instância de armazenamento de dados brutos com base no tipo especificado, usando o tipo de dado fornecido para configurar a instância corretamente.

        Args:
            storage_type (str): Tipo de armazenamento a ser criado (por exemplo, "json").
            data_type (str): Tipo de dado referente ao indicador que chamou a fábrica (por exemplo, "cdi").

        Returns:
            BaseRawStorage: Instância de armazenamento de dados brutos criada com base no tipo especificado.
        """
        storage_map = {
            "json": JsonRawStorage,
        }

        storage_class = storage_map.get(storage_type.lower())
        if not storage_class:
            raise ValueError(f"Tipo de persistência de dados brutos desconhecido: {storage_type}")

        return storage_class(data_type)
