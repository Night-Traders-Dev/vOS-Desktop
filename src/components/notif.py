from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.events import Click
from textual.geometry import Offset
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static
import asyncio

class BarContainer(Container):
    """Topbar Container"""
    time = reactive(0)

    def update_timer(self) -> None:
        self.time += 1

    def watch_time(self, time: int) -> None:
        if time == 3:
            self.timer.pause()
            self.time = 0
            self.parent.styles.animate("width", value=0, duration=1/6)
            self.parent.styles.animate("height", value=0, duration=1/6)
            self.parent.styles.animate("opacity", value=0.0, duration=1/6, on_complete=self.remove)

    def on_mount(self) -> None:
        self.timer = self.set_interval(1, self.update_timer)


class TitleText(Static):
    """TitleText Widget"""

class Window(Vertical):

    DEFAULT_CSS = """
    Window {
        overlay: screen;
        dock: left;
        layout: vertical;
        content-align: center middle;
        background: rgba(51, 51, 51, 0.50);
    }
     Window #title-bar {
        width: 100%;
        height: 1;
        background: rgba(244, 170, 144, 0.50);
        dock: top;
        layout: horizontal;
    }

    Window #title  {
        dock: top;

    }
    """

    def __init__(self, x: int, y: int, width: int, height: int, label: str, title: str) -> None:
        super().__init__()
        self.offset = Offset(x, y)
        self.styles.width = width
        self.styles.height = height
        self.label = label
        self.title = title
#        self.id = id


    def render(self) -> str:
        return self.label

    def set_title(self, new_title: str):

        title_bar = self.query_one("#title-bar")
        title_text = title_bar.query_one("#title")

        old_text = title_text.renderable.plain

        title_text.update(f" [bold]{new_title}[/bold]")

    async def _on_click(self, event: Click) -> None:
        self.styles.animate("width", value=0, duration=1/6)
        self.styles.animate("height", value=0, duration=1/6)
        self.styles.animate("opacity", value=0.0, duration=1/6, on_complete=self.remove)


    def compose(self) -> ComposeResult:
        with BarContainer(id="title-bar"):
            yield TitleText(f" [bold]{self.title}[/bold]", id="title")

    def on_mount(self) -> None:
        self.styles.animate("width", value=20, duration=1/6)
        self.styles.animate("height", value=5, duration=1/6)


