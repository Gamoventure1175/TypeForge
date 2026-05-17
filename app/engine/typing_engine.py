from time import time, perf_counter
from .utils import calculate_accuracy, calculate_wpm, count_correct_chars
from models import (
    BackspacePressed,
    CharacterTyped,
    Event,
    SessionState,
    TestFinished,
    TestQuit,
    TypingState,
    TypingStats,
)
from dataclasses import replace
from .policies.typing_policies import TypingPolicy


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
        "Completes the typing test and returns the finished state"
        if state.session_state == SessionState.FINISHED:
            return state

        self._end_time = time()

        new_state = replace(state, session_state=SessionState.FINISHED)

        return self._build_state(new_state, "")

    def process_char(self, state: TypingState, char: str) -> TypingState:
        """
        Process a typed character and return a new immutable typing state
        """

        if len(char) != 1:
            raise ValueError("Only a single characters allowed to be typed")

        if state.session_state == SessionState.FINISHED:
            raise RuntimeError("Cannot type after a test is finished.")

        if self._start_time is None:
            self._start_time = time()

        # Don't allow typing beyond chars in target
        if len(state.typed) >= len(state.target):
            return self.finish(state)

        new_typed = state.typed + char
        temp_state = replace(state, session_state=SessionState.RUNNING)

        new_state = self._build_state(temp_state, new_typed)

        return new_state

    def process_backspace(self, state: TypingState) -> TypingState:
        "Handles backspace transition"
        if state.session_state == SessionState.FINISHED:
            return state

        if not state.typed:
            return state

        new_typed = state.typed[:-1]
        temp_state = replace(state, session_state=SessionState.RUNNING)

        return self._build_state(temp_state, new_typed)

    # TODO: implement the actual test quiting behaviour
    def quit(self, state: TypingState) -> TypingState:
        "Aborts / Quits the test"
        ...

    def calculate_stats(self, state: TypingState) -> TypingStats:
        "Calculate derived typing statistics"
        correct_chars = count_correct_chars(state.target, state.typed)

        elapsed = self._get_elapsed_time()

        accuracy = calculate_accuracy(correct_chars, len(state.typed))

        wpm = calculate_wpm(correct_chars, elapsed)

        return TypingStats(correct_chars, accuracy, wpm)

    def process_event(self, state: TypingState, event: Event) -> TypingState:
        match event:

            case CharacterTyped(char):
                return self.process_char(state, event.char)

            case BackspacePressed():
                return self.process_backspace(state)

            case TestFinished():
                return self.finish(state)

            case TestQuit():
                return self.finish(state)

            case _:
                raise ValueError(f"Unhandled event: {event}")

    def _build_state(self, previous_state: TypingState, typed: str) -> TypingState:
        "Centralized state derivation pipeline"
        temp_state = replace(previous_state, typed=typed)

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

        end = self._end_time or time()

        return end - self._start_time
