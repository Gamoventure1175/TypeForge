# ----------------- STATS ----------------------
def calculate_accuracy(correct_chars: int, total_typed: int) -> float:
    if total_typed <= 0:
        return 0
    return correct_chars / total_typed * 100


def calculate_wpm(correct_chars: int, elapsed_seconds: float) -> float:
    if elapsed_seconds == 0:
        return 0
    return (correct_chars / 5) / (elapsed_seconds / 60)


# ----------------- EVALUATION ----------------------
def count_correct_chars(target: str, typed: str) -> int:
    return sum(1 for i, ch in enumerate(typed) if i < len(target) and ch == target[i])


def evaluate_characters(target: str, typed: str) -> list[tuple[str, bool]]:
    return [(ch, i < len(target) and ch == target[i]) for i, ch in enumerate(typed)]
