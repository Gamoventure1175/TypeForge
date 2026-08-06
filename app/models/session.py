from enum import Enum
from dataclasses import dataclass
from models.typing import TypingState, TypingStats
from models.events import Event


class SessionLifecycle(Enum):
    IDLE = "idle"
    RUNNING = "running"
    FINISHED = "finished"
    ABORTED = "aborted"


@dataclass(frozen=True)
class SessionSnapShot:
    state: TypingState
    stats: TypingStats
    lifecycle: SessionLifecycle
    event_history: tuple[Event]
    elapsed_time: float
