from dataclasses import dataclass


@dataclass(frozen=True)
class ComponentID:
    """Classe base para IDs de componentes Dash."""
    value: str

    def __str__(self) -> str:
        return self.value


class DropdownIDs:
    pass


class GraphIDs:
    pass


class ButtonIDs:
    pass
