from dataclasses import replace
from time import perf_counter
from models import (
    SessionState,
    TypingState,
    TypingStats,
)
from utils.typing_utils import calculate_accuracy, calculate_wpm, count_correct_chars
from events import Event, CharacterTyped, BackspacePressed, EscPressed
from policies.typing_policies import setup_policy


class TypingEngine:
    def __init__(self):
        self._start_time: float | None = None
        self._end_time: float | None = None
        self._last_input_time: float | None = None

    def start(self):
        "Starts the current session for the typing test"
        now = perf_counter()
        self._start_time = now
        self._last_input_time = now

    def finish(self, state: TypingState) -> TypingState:
        "Ends the current session for the typing test"
        if state.session_state == SessionState.FINISHED:
            return state

        self._end_time = perf_counter()

        return self._build_state(state, session_state=SessionState.FINISHED)

    def process_char(self, state: TypingState, char: str) -> TypingState:
        """
        Process a typed character and return a new immutable typing state
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

    def process_backspace(self, state: TypingState) -> TypingState:
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

    def quit(self, state: TypingState) -> TypingState:
        "Aborts / Quits the test"
        if not self._start_time:
            raise ValueError("Cannot quit a null session")

        self._end_time = perf_counter()

        return self._build_state(state, session_state=SessionState.ABORTED)

    def calculate_stats(self, state: TypingState) -> TypingStats:
        "Calculate derived typing statistics"
        correct_chars = count_correct_chars(state.target, state.typed)

        elapsed = self._get_elapsed_time()

        accuracy = calculate_accuracy(correct_chars, len(state.typed))

        wpm = calculate_wpm(correct_chars, elapsed)

        return TypingStats(correct_chars, accuracy, wpm)

    def _build_state(self, previous_state: TypingState, **changes) -> TypingState:
        "Centralized state derivation pipeline"
        temp_state = replace(previous_state, **changes)

        stats = self.calculate_stats(temp_state)

        return replace(
            temp_state,
            correct_chars=stats.correct_chars,
            accuracy=stats.accuracy,
            wpm=stats.wpm,
        )

    def _get_elapsed_time(self) -> float:
        """
        Return elapsed typing duration.
        """

        if self._start_time is None:
            return 0

        end = self._end_time or perf_counter()

        return end - self._start_time


# class Controller:
#     def __init__(self):
#         self._typing_engine = _TypingEngine()
#         self._typing_policies = setup_policy()
#
#     def process_event(event: Event) -> TypingState:
#         pass
