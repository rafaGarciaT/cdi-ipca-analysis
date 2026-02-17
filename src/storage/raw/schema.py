from typing import TypedDict


class RawDataPayload(TypedDict):
    reference_date: str
    type: str
    value: float
