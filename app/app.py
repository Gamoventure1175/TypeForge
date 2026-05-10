from textual.app import App

from screens import TypingScreen


class TypingApp(App):
    def on_mount(self):
        self.push_screen(TypingScreen())
