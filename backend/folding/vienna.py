from .base import FoldResult

class ViennaRNAEngine:
    name = "viennarna"

    def fold(self, sequence: str) -> FoldResult:
        raise NotImplementedError(
            "ViennaRNA will be installed and connected in the next project stage."
        )
