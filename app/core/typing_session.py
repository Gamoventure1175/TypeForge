from core.typing_engine import TypingEngine
from models.typing_models import SessionState, TypingState, TypingStats
from policies.typing_policies import TypingPolicy


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

        self._events = []

        self._session_state = SessionState.IDLE

        self._start_time = None
        self._end_time = None
        self._last_input = None
