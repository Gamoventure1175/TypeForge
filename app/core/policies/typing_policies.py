from dataclasses import dataclass, replace


@dataclass(frozen=True)
class TypingPolicy:
    allow_leading_spaces: bool = False
    allow_consecutive_spaces: bool = False
    allow_backspace: bool = True
    allow_quit: bool = False


def setup_policy(
    leading_spaces=False,
    consecutive_spaces=False,
    allow_backspace=False,
    allow_quit=False,
) -> TypingPolicy:
    return TypingPolicy(
        leading_spaces,
        consecutive_spaces,
        allow_backspace,
        allow_quit,
    )


def update_policy(policy: TypingPolicy, **changes) -> TypingPolicy:
    return replace(policy, **changes)
