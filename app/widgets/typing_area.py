from textual import events
from textual.widgets import Static

from core.session import TypingSession
from core.policies.typing import setup_policy
from models.events import CharacterTyped, BackspacePressed, EscPressed
from models.typing import TypingState, TypingStats
from models.session import SessionLifecycle


class TypingArea(Static):
    can_focus = True

    def __init__(self):
        super().__init__()

        self.policy = setup_policy()
        self.state = TypingState(
            target="Some plastic chairs sat under a glowing yellow moon while a lonely cat chased shadows across the dusty street.",
            typed="",
        )
        self.session = TypingSession(self.policy, self.state)
        self.stats = TypingStats(correct_chars=0, accuracy=0, wpm=0)

    def on_mount(self):
        self.focus()

    def on_key(self, event: events.Key):
        if self.session.lifecycle in (
            SessionLifecycle.ABORTED,
            SessionLifecycle.FINISHED,
        ):
            return

        # ESC quits test
        if event.key == "escape":
            domain_event = EscPressed()

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
        try:
            self.session.process(domain_event)
        except Exception as e:
            print(e)

        snapshot = self.session.snapshot
        self.state = snapshot.state
        self.stats = snapshot.stats

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
            f"WPM: {int(self.stats.wpm)}\n"
            f"Accuracy: {int(self.stats.accuracy)}%"
        )
