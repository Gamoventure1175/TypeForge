from dataclasses import dataclass


@dataclass(frozen=True)
class RenderCharacter:
    char: str
    correct: bool
    current: bool


@dataclass(frozen=True)
class TypingRenderState:
    characters: list[RenderCharacter]
    wpm: int
    accuracy: int
    session_state: str
