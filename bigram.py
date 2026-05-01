import random
from collections import defaultdict

MODEL_TEXT = "shakespeare.txt"
SEED_CHAR = "t"
OUTPUT_LENGTH = 500


def build_bigram_probabilities(text: str) -> dict[str, dict[str, float]]:
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for current_char, next_char in zip(text, text[1:]):
        counts[current_char][next_char] += 1

    probabilities: dict[str, dict[str, float]] = {}
    for current_char, current_char_sucessors in counts.items():
        total = sum(current_char_sucessors.values())
        probabilities[current_char] = {
            key: value / total for key, value in current_char_sucessors.items()
        }
    return probabilities


def validate_probs(probabilities: dict[str, dict[str, float]]) -> None:
    for char, row in probabilities.items():
        total = sum(row.values())
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"row {char!r} sums to {total}, expected 1.0")


def generate(probabilities: dict[str, dict[str, float]], seed: str, length: int) -> str:
    current = seed
    output = [seed]
    for _ in range(length):
        successors = probabilities[current]
        current = random.choices(list(successors.keys()), list(successors.values()))[0]
        output.append(current)
    return "".join(output)


if __name__ == "__main__":
    with open(MODEL_TEXT) as f:
        text = f.read().lower()

    built_probabilities = build_bigram_probabilities(text)
    validate_probs(built_probabilities)
    print(generate(built_probabilities, seed=SEED_CHAR, length=OUTPUT_LENGTH))
