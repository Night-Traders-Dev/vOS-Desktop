from textual.app import App, ComposeResult
from textual.containers import Center, Vertical
from textual.widgets import Label

class Icon(Vertical):

    DEFAULT_CSS = """
    Icon {
        visibility: hidden;
        width: 10;
        height: 10;

        Center {
            margin-bottom: 1;
            content-align: center middle;
        }

        Label {
            visibility: visible;
        }
    }
    """

    def __init__(self, label: str) -> None:
        super().__init__()
        self._label = label

    def compose(self) -> ComposeResult:
        with Center():
            yield Label("▉▉▉▉\n▉▉▉▉\n▉▉▉▉", classes="image")
        yield Label(self._label)

class IconLikeApp(App[None]):

    CSS = """
    Screen {
        layers: background foreground;
        layout: horizontal;
    }

    #background {
        width: 100%;
        height: 100%;
        color: #444;
        overflow: hidden;
        layer: background;
        background: rgb(119, 41, 83);
    }

    Icon {
        layer: foreground;
    }
    """

    def compose(self) -> ComposeResult:
        yield Label("" * 1000, id="background")
        for n in range(5):
            yield Icon(f"Icon {n}")

if __name__ == "__main__":
    IconLikeApp().run()
