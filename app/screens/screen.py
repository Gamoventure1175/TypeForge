from textual.app import ComposeResult
from textual.screen import Screen

from widgets.typing_area import TypingArea


class TypingScreen(Screen):
    def compose(self) -> ComposeResult:
        yield TypingArea()
