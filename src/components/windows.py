from textual.containers import Vertical
from textual.css.scalar import ScalarOffset, Scalar, Unit
from textual.events import Click
from textual.geometry import Offset
from textual.widget import Widget
from textual.widgets import Static
from .containers import BarContainer
import shutil

class TitleText(Static):
    """TitleText Widget"""
    def on_resize(self) -> None:
        bounds = shutil.get_terminal_size()
        title_bar = self.parent.parent.query_one("#title-bar")
        title_text = title_bar.query_one("#title")
        if title_bar.is_maximized:
            title_text.styles.content_align = ("center", "top")
        else:
            title_text.styles.content_align = ("right", "top")

class Window(Vertical):

    DEFAULT_CSS = """
    Window {
        overlay: screen;
        dock: left;
        layout: vertical;
        content-align: center middle;
        background: rgba(119, 41, 83, 0.75);
    }
     Window #title-bar {
        width: 100%;
        height: 1.50;
        background: rgba(51, 51, 51, 0.50);
        dock: top;
        layout: horizontal;
    }

    Window #title  {
        dock: top;
        content-align: right top;
    }
    """

    def __init__(self, x: int, y: int, width: int, height: int, label: str, title: str, id: str | None = None) -> None:
        super().__init__()
        self.offset = Offset(x, y)
        self.width = width
        self.height = height
        self.label = label
        self.title = title
        self.id = id

    def on_mount(self) -> None:
        self.styles.width = 0
        self.styles.height = 0
        self.styles.animate("width", value=self.width, duration=1/6)
        self.styles.animate("height", value=self.height, duration=1/6)

    def render(self) -> str:
        return self.label

    def set_title(self, new_title: str):
        title_bar = self.query_one("#title-bar")
        title_text = title_bar.query_one("#title")
        title_text.update(f" [bold]{new_title}[/bold]")

    async def _on_click(self, event: Click) -> None:
        if isinstance(self.parent, Widget):
            self.focus()
            self.parent.move_child(self, after=-1)
            return await super()._on_click(event)

    def compose(self):
        with BarContainer(id="title-bar"):
            yield TitleText(f" [bold]{self.title}[/bold]", id="title")
