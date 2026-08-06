from textual.app import App

from screens.screen import TypingScreen


class TypingApp(App):
    def on_mount(self):
        self.push_screen(TypingScreen())
