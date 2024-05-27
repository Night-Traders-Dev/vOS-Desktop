from textual.app import App, ComposeResult
from textual.containers import Container
from textual.events import Click
from textual.geometry import Offset
from textual.widget import Widget
from textual.widgets import Placeholder, Static

class BarContainer(Container):
    """Topbar Container"""

    def on_click(self, event: Click) -> None:
        self.parent.remove()

class Window(Placeholder):

    DEFAULT_CSS = """
    Window {
        overlay: screen;
        dock: left;
        layout: vertical;
    }
    #title-bar {
        width: 100%;
        height: 1;
        background: rgba(51, 51, 51, 0.50);
        dock: top;
        layout: horizontal;
    }

    """

    def __init__(self, x: int, y: int, width: int, height: int, label: str, title: str, id: str | None = None) -> None:
        super().__init__()
        self.offset = Offset(x, y)
        self.styles.width = width
        self.styles.height = height
        self.label = label
        self.title = title
        self.id = id


    def render(self) -> str:
        return self.label

    def compose(self) -> ComposeResult:
        with BarContainer(id="title-bar"):
            yield Static(f" [bold]{self.title}[/bold]", id="title")

    async def _on_click(self, event: Click) -> None:
        if isinstance(self.parent, Widget):
            self.focus()
            self.parent.move_child(self, after=-1)
            return await super()._on_click(event)

class WindowTemplate(App[None]):
    def compose(self) -> ComposeResult:
        yield Window(3, 3, 20, 10, f"some emojis", "Emojis", "emoji")
        yield Window(4, 7, 20, 5, f"A random dialog", "Dialog", "dialog")
        yield Window(7, 10, 20, 5, f"Some cool notification", "Notification", "notification") 

if __name__ == "__main__":
    WindowTemplate().run()
