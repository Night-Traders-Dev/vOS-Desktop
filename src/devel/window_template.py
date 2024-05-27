from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.events import Click
from textual.geometry import Offset
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static
from random import randint

class BarContainer(Container):
    """Topbar Container"""
    def on_click(self, event: Click) -> None:
        self.parent.remove()

class TitleText(Static):
    """TitleText Widget"""

class Window(Vertical):

    DEFAULT_CSS = """
    Window {
        overlay: screen;
        dock: left;
        layout: vertical;
        content-align: center middle;
        background: rgba(119, 41, 83, 0.50);
    }
     Window #title-bar {
        width: 100%;
        height: 1;
        background: rgba(51, 51, 51, 0.50);
        dock: top;
        layout: horizontal;
    }

    Window #title  {
        dock: top;

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

    def set_title(self, new_title: str):

        title_bar = self.query_one("#title-bar")
        title_text = title_bar.query_one("#title")

        old_text = title_text.renderable.plain

        title_text.update(f" [bold]{new_title}[/bold]")

    async def _on_click(self, event: Click) -> None:
        if isinstance(self.parent, Widget):
            self.focus()
            self.parent.move_child(self, after=-1)
            return await super()._on_click(event)

    def compose(self) -> ComposeResult:
        with BarContainer(id="title-bar"):
            yield TitleText(f" [bold]{self.title}[/bold]", id="title")

class WindowTemplate(App[None]):
    def compose(self) -> ComposeResult:
        x, y = self.size
        win_x = randint(0, (x - 30))
        win_y = randint(0, (y - 20))
        yield Window((win_x), (win_y), 30, 20, f"\nBasic Window Content", "vOS UI", "window") 

if __name__ == "__main__":
    WindowTemplate().run()
