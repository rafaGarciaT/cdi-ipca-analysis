from typing import TypedDict, Union


class RawDataPayload(TypedDict):
    reference_date: str
    type: str
    value: Union[float, dict[str, float]]
