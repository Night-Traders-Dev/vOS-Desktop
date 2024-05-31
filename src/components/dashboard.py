from textual.app import App, ComposeResult
from textual.containers import Container, Vertical
from textual.css.scalar import ScalarOffset, Scalar, Unit
from textual.events import Click
from textual.geometry import Offset, Region
from textual.reactive import Reactive
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
            self.parent.styles.animate("width", value=width, duration=1/6)
            self.parent.styles.animate("height", value=height, duration=1/6)
            self.parent.styles.animate("offset", value=Window.get_center(width, height), duration=1/6)
            self.is_maximized = True
        else:
            self.parent.styles.animate("width", value=50, duration=1/6)
            self.parent.styles.animate("height", value=20, duration=1/6)
            self.parent.styles.animate("offset", value=Window.get_center(50, 20), duration=1/6)
            self.is_maximized = False


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

    current_screen_size: Reactive[tuple] = Reactive((0, 0))
    previous_screen_size: Reactive[tuple] = Reactive((0, 0))
    current_window_size: Reactive[tuple] = Reactive((0, 0))
    previous_window_size: Reactive[tuple] = Reactive((0, 0))

    DEFAULT_CSS = """
    Window {
        overlay: screen;
        dock: left;
        layout: grid;
        grid-size: 3 3;
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
    Window .box {
        height: 1fr;
        width: 1fr;
        border: solid rgba(233, 84, 32, 0.2);
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

    @staticmethod
    def get_center(width, height) -> None:
        bounds = shutil.get_terminal_size()
        screen_width = bounds.columns
        screen_height = bounds.lines
        center_x = screen_width // 2
        center_y = screen_height // 2
        center_x = center_x - (width // 2)
        center_y = center_y - (height // 2)

        new_offset = ScalarOffset(
            Scalar(center_x, Unit(1), Unit(1)),
            Scalar(center_y, Unit(1), Unit(1))
        )

        return new_offset

    @staticmethod
    def calculate_new_dimensions(old_screen_size, new_screen_size, old_widget_size):
        old_screen_width, old_screen_height = old_screen_size
        new_screen_width, new_screen_height = new_screen_size
        old_widget_width, old_widget_height = old_widget_size

        width_scale = new_screen_width / old_screen_width
        height_scale = new_screen_height / old_screen_height

        new_widget_width = int(old_widget_width * width_scale)
        new_widget_height = int(old_widget_height * height_scale)

        return new_widget_width, new_widget_height


    @staticmethod
    def get_screen_size():
        bounds = shutil.get_terminal_size()
        screen_width = bounds.columns
        screen_height = bounds.lines
        return (screen_width, screen_height)

    @staticmethod
    def animation_logic():
        pass
        self.styles.animate("width", value=new_width, duration=1/6)
        self.styles.animate("height", value=new_height, duration=1/6)
        self.styles.animate("offset", value=self.get_center(new_width, new_height), duration=1/6)

    def on_resize(self) -> None:
        self.previous_screen_size = self.current_screen_size
        self.current_screen_size = self.get_screen_size()
        self.previous_window_size = self.current_window_size
        self.current_window_size = self.size

    def watch_current_screen_size(self, current_screen_size: tuple):
        if self.previous_screen_size == (0, 0):
            self.previous_screen_size = self.current_screen_size
        new_width, new_height = self.calculate_new_dimensions(self.previous_screen_size, self.current_screen_size, self.previous_window_size)
        self.styles.animate("width", value=new_width, duration=1/6)
        self.styles.animate("height", value=new_height, duration=1/6)
        self.styles.animate("offset", value=self.get_center(new_width, new_height), duration=1/6)

    def on_mount(self) -> None:
        self.current_screen_size = self.get_screen_size()
        self.previous_screen_size = self.current_screen_size
        self.current_window_size = self.size
        self.styles.width = 0
        self.styles.height = 0
        self.styles.animate("width", value=self.width, duration=1/6)
        self.styles.animate("height", value=self.height, duration=1/6)
        self.styles.animate("offset", value=self.get_center(self.width, self.height), duration=1/6)


    def render(self) -> str:
        return self.label

    def set_title(self, new_title: str):

        title_bar = self.query_one("#title-bar")
        title_text = title_bar.query_one("#title")

        old_text = title_text.renderable.plain

        title_text.update(f" [bold]{new_title}[/bold]")

    def compose(self) -> ComposeResult:
        with BarContainer(id="title-bar"):
            yield TitleText(f" [bold]{self.title}[/bold]", id="title")
        yield Static("App One", classes="box")
        yield Static("App Two", classes="box")




