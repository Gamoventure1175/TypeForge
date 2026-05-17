from models import TypingState
from engine.policies.typing_policies import TypingPolicy
from engine.utils.typing_utils import (
    exceeds_target_length,
    is_double_space,
    is_leading_space,
)


def is_valid_transition(
    policy: TypingPolicy,
    target: str,
    typed: str,
) -> bool:

    if not policy.allow_leading_spaces and is_leading_space(typed):
        return False

    if not policy.allow_consecutive_spaces and is_double_space(typed):
        return False

    if not policy.allow_extra_characters and exceeds_target_length(typed, target):
        return False

    return True
