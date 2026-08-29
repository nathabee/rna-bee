from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class FoldResult:
    sequence: str
    structure: str
    free_energy_kcal_mol: float
    engine: str

class FoldingEngine(Protocol):
    name: str

    def fold(self, sequence: str) -> FoldResult:
        ...
