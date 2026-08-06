from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class TypingState:
    target: str
    typed: str

    @property
    def cursor(self) -> int:
        return len(self.typed)


@dataclass(frozen=True)
class TypingStats:
    "Stats = derived values"

    correct_chars: int
    accuracy: float
    wpm: float

    def __post_init__(self):
        if not (0 <= self.accuracy <= 100):
            raise ValueError(
                f"Accuracy needs to be between 0 to 100. Value: {self.accuracy}"
            )
