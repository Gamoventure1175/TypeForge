from textual.app import ComposeResult
from textual.screen import Screen

from widgets import TypingWidget


class TypingScreen(Screen):

    def compose(self) -> ComposeResult:
        yield TypingWidget()
