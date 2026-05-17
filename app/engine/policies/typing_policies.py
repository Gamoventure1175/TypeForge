from dataclasses import dataclass


@dataclass(frozen=True)
class TypingPolicy:
    allow_extra_characters: bool = False
    allow_leading_spaces: bool = False
    allow_word_skipping: bool = False
