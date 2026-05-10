from textual.widgets import Static
from textual import events

from engine import TypingEngine
from models import (
    CharacterTyped,
    BackspacePressed,
    TestQuit,
)
from models import TypingState


class TypingWidget(Static):

    can_focus = True

    def __init__(self):
        super().__init__()

        self.engine = TypingEngine()

        self.state = TypingState(
            target="hello world",
            typed="",
            correct_chars=0,
            accuracy=0,
            wpm=0,
            is_finished=False,
        )

    def on_mount(self):
        self.focus()

    def on_key(self, event: events.Key):

        # ESC quits test
        if event.key == "escape":
            domain_event = TestQuit()

        # Backspace
        elif event.key == "backspace":
            domain_event = BackspacePressed()

        # Ignore tab
        elif event.key == "tab":
            return

        # Regular characters
        elif event.character and len(event.character or "") == 1:
            domain_event = CharacterTyped(event.character)

        else:
            return

        # Process event through engine
        self.state = self.engine.process_event(
            self.state,
            domain_event,
        )

        # Refresh UI
        self.refresh()

    def render(self):

        typed_render = []

        for i, ch in enumerate(self.state.target):

            if i < len(self.state.typed):

                typed_char = self.state.typed[i]

                if typed_char == ch:
                    typed_render.append(f"[green]{typed_char}[/]")
                else:
                    typed_render.append(f"[red]{typed_char}[/]")

            else:
                typed_render.append(f"[dim]{ch}[/]")

        rendered_text = "".join(typed_render)

        return (
            f"{rendered_text}\n\n"
            f"WPM: {int(self.state.wpm)}\n"
            f"Accuracy: {int(self.state.accuracy)}%"
        )
