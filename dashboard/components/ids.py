from dataclasses import dataclass


@dataclass(frozen=True)
class ComponentID:
    """Classe base para IDs de componentes Dash."""
    value: str

    def __str__(self) -> str:
        return self.value

class InputIDs:
    INITIAL_AMOUNT = ComponentID("initial-amount")

class DropdownIDs:
    pass


class GraphIDs:
    pass


class ButtonIDs:
    CALCULATE = ComponentID("calculate-button")

class DatePickerIDs:
    START_YEAR = ComponentID("start-year")
    END_YEAR = ComponentID("end-year")
