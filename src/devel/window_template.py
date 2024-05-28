from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.css.scalar import ScalarOffset, Scalar, Unit
from textual.events import Click
from textual.geometry import Offset, Region
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static
from random import randint
from time import time
from threading import Timer
import shutil



class BarContainer(Container):
    """Topbar Container"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.last_click_time = 0
        self.double_click_threshold = 0.3
        self.is_maximized = False
        self.resize_timer = None

    def on_click(self, event: Click) -> None:
        current_time = time()
        time_since_last_click = current_time - self.last_click_time

        if time_since_last_click <= self.double_click_threshold:
            self.on_double_click(event)
        else:
            self.resize_timer = self.set_timer(0.25, self.on_single_click)
            self.resize_timer = None

        self.last_click_time = current_time

    def on_single_click(self) -> None:
        bounds = shutil.get_terminal_size()

        if not self.is_maximized:
            width = bounds.columns
            height = bounds.lines
            x = 0
            y = 0
            self.is_maximized = True
        else:
            width = 30
            height = 20
            x = 0
            y = 0
            self.is_maximized = False

        self.parent.styles.animate("width", value=width, duration=1/6)
        self.parent.styles.animate("height", value=height, duration=1/6)
        new_offset = ScalarOffset(
            Scalar(x, Unit(1), Unit(1)),
            Scalar(y, Unit(1), Unit(1))
        )
        self.parent.styles.animate("offset", value=new_offset, duration=1/6)

    def on_double_click(self, event: Click) -> None:
        if self.parent:
            self.parent.styles.animate("opacity", value=0.0, duration=1/6, on_complete=self.parent.remove)

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
        self.styles.width = width
        self.styles.height = height
        self.label = label
        self.title = title
        self.id = id


    def on_mount(self) -> None:
        self.styles.animate("width", value=30, duration=1/6)
        self.styles.animate("height", value=20, duration=1/6)


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

    def on_mount(self) -> None:
        self.notify("Press tap or click anywhere to open a test window")
    def on_click(self) -> None:
        try:
            if self.query_one("#window"):
                pass
        except:
            x, y = self.size
            win_x = randint(0, (x - 30))
            win_y = randint(0, (y - 20))
            self.mount(Window((win_x), (win_y), 0, 0, f"\nBasic Window Content", "vOS UI", "window"))


if __name__ == "__main__":
    WindowTemplate().run()
