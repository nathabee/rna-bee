import random

RNA_ALPHABET = ("A", "U", "G", "C")

def random_sequence(length: int, rng: random.Random | None = None) -> str:
    if length <= 0:
        raise ValueError("length must be greater than zero")
    rng = rng or random
    return "".join(rng.choice(RNA_ALPHABET) for _ in range(length))
