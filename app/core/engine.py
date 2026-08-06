from dataclasses import replace

from models.typing import TypingState
from models.events import Event, CharacterTyped, BackspacePressed


class StateTransitionEngine:
    def _process_char(self, state: TypingState, char: str) -> TypingState:
        """
        Handles chracter transition
        """
        if len(char) != 1:
            raise ValueError("Only a single characters allowed to be typed")

        return self._build_state(state, typed=state.typed + char)

    def _process_backspace(self, state: TypingState) -> TypingState:
        "Handles backspace transition"
        if not state.typed:
            return state

        return self._build_state(state, typed=state.typed[:-1])

    def _build_state(self, previous_state: TypingState, **changes):
        return replace(previous_state, **changes)

    def process_event(
        self,
        state: TypingState,
        event: Event,
    ) -> TypingState:
        match event:
            case CharacterTyped(char):
                return self._process_char(state, char)
            case BackspacePressed():
                return self._process_backspace(state)

        return state
