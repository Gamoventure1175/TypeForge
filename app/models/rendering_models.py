from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RenderCharacter:
    char: str
    correct: bool
    current: bool


@dataclass(frozen=True)
class TypingRenderState:
    characters: List[RenderCharacter]
    wpm: int
    accuracy: int
    session_state: str
