from textual.containers import Container
from textual.events import Click
from textual.css.scalar import ScalarOffset, Scalar, Unit
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
            width = self.parent.width
            height = self.parent.height
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
