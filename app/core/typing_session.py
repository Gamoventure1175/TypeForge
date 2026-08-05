from time import perf_counter

from core.typing_engine import TypingEngine
from models.typing_models import (
    SessionEnded,
    SessionState,
    SessionStarted,
    TypingState,
    TypingStats,
)
from models.events import Event
from policies.typing_policies import TypingPolicy, is_valid_transition
from utils.typing_utils import count_correct_chars, calculate_accuracy, calculate_wpm


class _Typing_Session:
    def __init__(self, policy: TypingPolicy, state: TypingState):
        self._engine = TypingEngine()

        self._typing_state = state
        self._typing_stats = TypingStats(
            correct_chars=0,
            accuracy=0,
            wpm=0,
        )

        self._policy = policy

        self._event_history = []

        self._session_state = SessionState.IDLE

        self._start_time = None
        self._end_time = None
        self._last_input = None

    def _is_first_event(self) -> bool:
        return self._session_state is SessionState.IDLE and not self._event_history

    def _should_finish(self) -> bool:
        return len(self._typing_state.typed) >= len(self._typing_state.target)

    def _start_session(self):
        self._start_time = perf_counter()
        self._event_history.append(SessionStarted())

    def _end_session(self):
        self._end_time = perf_counter()
        self._event_history.append(SessionEnded())

    def _get_elapsed_time(self) -> float:
        if self._start_time is None:
            return 0

        end = self._end_time or perf_counter()

        return end - self._start_time

    def _refresh_stats(self):
        self._typing_stats = self._calculate_stats(self._typing_state)

    def _calculate_stats(self, state: TypingState) -> TypingStats:
        "Calculate derived typing statistics"
        correct_chars = count_correct_chars(state.target, state.typed)

        elapsed = self._get_elapsed_time()

        accuracy = calculate_accuracy(correct_chars, len(state.typed))

        wpm = calculate_wpm(correct_chars, elapsed)

        return TypingStats(correct_chars, accuracy, wpm)

    def process_session_event(self, event: Event): 
        if self._is_first_event():
            self._start_session()

        if not is_valid_transition(self._policy, self._typing_state, event):
            return self._typing_state

        self._event_history.append(event)

        self._typing_state = self._engine.process_event(
            self._typing_state, event, self._policy
        )

        if self._typing_state.endp

        self._refresh_stats()


        if self._should_finish():
            self._typing_state()

