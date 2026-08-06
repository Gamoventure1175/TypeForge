from models.typing import TypingState
from core.policies.typing import TypingPolicy
from models.events import Event, CharacterTyped, BackspacePressed, EscPressed


def is_valid_transition(
    policy: TypingPolicy, previous_state: TypingState, event: Event
) -> bool:
    match event:
        case CharacterTyped(char):
            if (
                not policy.allow_leading_spaces
                and not previous_state.typed
                and char == " "
            ):
                return False

            if (
                not policy.allow_consecutive_spaces
                and previous_state.typed.endswith(" ")
                and char == " "
            ):
                return False

        case BackspacePressed():
            if not policy.allow_backspace:
                return False

        case EscPressed():
            if not policy.allow_quit:
                return False

    return True
