import random
from collections import defaultdict

MODEL_TEXT = "shakespeare.txt"
SEED_BIGRAM = "t"
SEED_TRIGRAM = "th"
OUTPUT_LENGTH = 500


def build_ngram_probabilities(text: str, n: int) -> dict[str, dict[str, float]]:
    counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for i in range(len(text) - n + 1):
        context, next_char = (
            text[i : i + n - 1],
            text[i + n - 1],
        )  # n-1 char context → 1 char prediction
        counts[context][next_char] += 1

    return {
        context: {
            key: value / sum(successors.values()) for key, value in successors.items()
        }
        for context, successors in counts.items()
    }


def validate_probs(probabilities: dict[str, dict[str, float]]) -> None:
    for char, row in probabilities.items():
        total = sum(row.values())
        if abs(total - 1.0) > 1e-9:
            raise ValueError(f"row {char!r} sums to {total}, expected 1.0")


def generate(
    probabilities: dict[str, dict[str, float]],
    seed: str,
    length: int,
) -> str:
    current = seed
    output = [seed]
    for _ in range(length):
        successors = probabilities[current]
        picked_char = random.choices(
            list(successors.keys()), list(successors.values())
        )[0]
        output.append(picked_char)
        current = current[1:] + picked_char
    return "".join(output)


if __name__ == "__main__":
    with open(MODEL_TEXT) as f:
        text = f.read().lower()

    for n, seed in [(2, SEED_BIGRAM), (3, SEED_TRIGRAM)]:
        probs = build_ngram_probabilities(text, n)
        validate_probs(probs)
        print(f"--- {n}-gram ---")
        print(generate(probs, seed=seed, length=OUTPUT_LENGTH))
