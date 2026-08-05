from time import perf_counter
from models import (
    SessionState,
    TypingState,
)
from events import Event, CharacterTyped, BackspacePressed, EscPressed
from policies.typing_policies import TypingPolicy
from validation.typing_policy_validation import is_valid_transition


class TypingEngine:
    def _process_char(self, state: TypingState, char: str) -> TypingState:
        """
        Handles chracter transition
        """

        if len(char) != 1:
            raise ValueError("Only a single characters allowed to be typed")

        if state.session_state == SessionState.FINISHED:
            raise RuntimeError("Cannot type after a test is finished.")

        # Don't allow typing beyond chars in target
        if len(state.typed) >= len(state.target):
            return self.finish(state)

        if self._start_time is None:
            self.start()

        new_typed = state.typed + char
        self._last_input_time = perf_counter()

        new_state = self._build_state(
            state, typed=new_typed, session_state=SessionState.RUNNING
        )

        return new_state

    def _process_backspace(self, state: TypingState) -> TypingState:
        "Handles backspace transition"
        if state.session_state == SessionState.FINISHED:
            return state

        if not state.typed:
            return state

        new_typed = state.typed[:-1]
        self._last_input_time = perf_counter()

        return self._build_state(
            state, typed=new_typed, session_state=SessionState.RUNNING
        )

    def _process_escape(self, state: TypingState) -> TypingState:
        "Handles escape transition"
        return self._build_state(state, session_state=SessionState.ABORTED)

    def _process_finish(self, state: TypingState) -> TypingState:
        "Handles session completion transition"
        return self._build_state(state, session_state=SessionState.FINISHED)

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
            case EscPressed():
                return self._process_escape(state)

        return self._process_finish(state)
