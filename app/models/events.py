from dataclasses import dataclass


@dataclass(frozen=True)
class Event:
    pass


@dataclass(frozen=True)
class CharacterTyped(Event):
    char: str


@dataclass(frozen=True)
class BackspacePressed(Event):
    pass


@dataclass(frozen=True)
class TestFinished(Event):
    pass


@dataclass(frozen=True)
class TestQuit(Event):
    pass
