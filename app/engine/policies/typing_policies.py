from dataclasses import dataclass, replace


@dataclass(frozen=True)
class TypingPolicy:
    allow_extra_characters: bool = False
    allow_leading_spaces: bool = False
    allow_consecutive_spaces: bool = False


def setup_policy(
    extra_characters=False,
    leading_spaces=False,
    consecutive_spaces=False,
    empty_word_progression=False,
) -> TypingPolicy:
    return TypingPolicy(extra_characters, leading_spaces, consecutive_spaces)


def update_policy(policy: TypingPolicy, **changes) -> TypingPolicy:
    return replace(policy, **changes)
