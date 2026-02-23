from typing import TypedDict, Union


class RawDataPayload(TypedDict):
    """Estrutura de dados para o payload de dados brutos."""
    reference_date: str
    type: str
    value: Union[float, dict[str, float]]
