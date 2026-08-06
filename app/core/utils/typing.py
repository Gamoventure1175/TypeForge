from models.events import BackspacePressed


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


# ----------------- WORDS ----------------------
def get_target_words(target: str) -> list[str]:
    return target.split()


def get_typed_words(typed: str) -> list[str]:
    return typed.split()


def get_current_word(typed: str) -> str:
    return typed.split()[-1] if typed.split() else ""


def just_completed_word(typed: str, char: str) -> bool:
    return bool(typed) and char == " "


def exceeds_target_length(typed: str, target: str) -> bool:
    return len(typed) > len(target)


# ----------------- SPACES ----------------------
def is_leading_space(typed: str) -> bool:
    return typed.startswith(" ")


def is_double_space(typed: str) -> bool:
    return "  " in typed


def is_backspace(event: None | BackspacePressed) -> bool:
    return bool(event)
