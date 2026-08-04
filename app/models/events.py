from dataclasses import dataclass, field
from time import perf_counter


@dataclass(frozen=True)
class Event:
    timestamp: float = field(default_factory=perf_counter)


@dataclass(frozen=True)
class CharacterTyped(Event):
    char: str


@dataclass(frozen=True)
class BackspacePressed(Event):
    pass


@dataclass(frozen=True)
class EscPressed(Event):
    pass


# @dataclass(frozen=True)
# class TestFinished(Event):
#     pass
#
#
# @dataclass(frozen=True)
# class TestQuit(Event):
#     pass
