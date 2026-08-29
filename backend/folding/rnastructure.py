from .base import FoldResult

class RNAstructureEngine:
    name = "rnastructure"

    def fold(self, sequence: str) -> FoldResult:
        raise NotImplementedError(
            "RNAstructure will be installed and connected in a later project stage."
        )
