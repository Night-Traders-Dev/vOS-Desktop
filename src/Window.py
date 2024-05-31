from components.window import Window
from textual.app import App, ComposeResult
from random import randint

class WindowTemplate(App[None]):

    def on_click(self) -> None:
        try:
            if self.query_one("#window"):
                pass
        except:
            x, y = self.size
            win_x = (x / 8)
            win_y = (x / 8)
            self.mount(Window((win_x), (win_y), 50, 20, f"", "vOS UI", "window"))


if __name__ == "__main__":
    WindowTemplate().run()
