import random

RNA_ALPHABET = ("A", "U", "G", "C")

def point_mutation(sequence: str, rng: random.Random | None = None) -> str:
    if not sequence:
        raise ValueError("sequence must not be empty")

    rng = rng or random
    position = rng.randrange(len(sequence))
    current = sequence[position]

    if current not in RNA_ALPHABET:
        raise ValueError("sequence contains a non-RNA base")

    replacement = rng.choice([b for b in RNA_ALPHABET if b != current])
    return sequence[:position] + replacement + sequence[position + 1:]
