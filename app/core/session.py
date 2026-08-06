from time import perf_counter

from core.engine import StateTransitionEngine
from models.events import EscPressed, Event, SessionEnded, SessionStarted
from models.session import SessionLifecycle, SessionSnapShot
from models.typing import (
    TypingState,
    TypingStats,
)
from core.policies.typing import TypingPolicy
from core.validation.transitions import is_valid_transition
from core.utils.typing import calculate_accuracy, calculate_wpm, count_correct_chars


class TypingSession:
    def __init__(self, policy: TypingPolicy, state: TypingState):
        self._engine = StateTransitionEngine()
        self._current_state = state
        self._stats = TypingStats(
            correct_chars=0,
            accuracy=0,
            wpm=0,
        )
        self._policy = policy
        self._event_history = []
        self._session_lifecycle = SessionLifecycle.IDLE
        self._start_time = None
        self._end_time = None
        self._last_input_time = None

    def _is_first_event(self) -> bool:
        return (
            self._session_lifecycle is SessionLifecycle.IDLE and not self._event_history
        )

    def _should_finish(self) -> bool:
        return len(self._current_state.typed) >= len(self._current_state.target)

    def _start_session(self):
        self._start_time = perf_counter()
        self._event_history.append(SessionStarted())
        self._session_lifecycle = SessionLifecycle.RUNNING

    def _end_session(
        self, lifecycle_change: SessionLifecycle = SessionLifecycle.FINISHED
    ):
        if self._session_lifecycle in (
            SessionLifecycle.FINISHED,
            SessionLifecycle.ABORTED,
        ):
            return
        self._end_time = perf_counter()
        self._event_history.append(SessionEnded())
        self._session_lifecycle = lifecycle_change

    def _get_elapsed_time(self) -> float:
        if self._start_time is None:
            return 0
        end = self._end_time or perf_counter()
        return end - self._start_time

    def _update_stats(self):
        self._stats = self._calculate_stats(self._current_state)

    def _calculate_stats(self, state: TypingState) -> TypingStats:
        "Calculate derived typing statistics"
        correct_chars = count_correct_chars(state.target, state.typed)
        elapsed = self._get_elapsed_time()
        accuracy = calculate_accuracy(correct_chars, len(state.typed))
        wpm = calculate_wpm(correct_chars, elapsed)
        return TypingStats(correct_chars, accuracy, wpm)

    def process(self, event: Event):
        if self._session_lifecycle in (
            SessionLifecycle.ABORTED,
            SessionLifecycle.FINISHED,
        ):
            return

        if not is_valid_transition(self._policy, self._current_state, event):
            return

        if self._is_first_event():
            self._start_session()

        self._last_input_time = event.timestamp
        self._event_history.append(event)

        if isinstance(event, EscPressed):
            self._end_session(SessionLifecycle.ABORTED)
            self._update_stats()
            return

        self._current_state = self._engine.process_event(self._current_state, event)

        if self._should_finish():
            self._end_session()

        self._update_stats()

    @property
    def state(self):
        return self._current_state

    @property
    def stats(self):
        return self._stats

    @property
    def event_history(self):
        return tuple(self._event_history)

    @property
    def lifecycle(self):
        return self._session_lifecycle

    @property
    def snapshot(self) -> SessionSnapShot:
        return SessionSnapShot(
            state=self._current_state,
            stats=self._stats,
            lifecycle=self._session_lifecycle,
            elapsed_time=self._get_elapsed_time(),
            event_history=tuple(self._event_history),
        )
