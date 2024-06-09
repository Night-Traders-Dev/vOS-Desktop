from rich.segment import Segment
from rich.style import Style
from textual.strip import Strip
from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Static
from textual.containers import Grid
from textual.geometry import Region
from textual.screen import Screen
from textual import on, events, work
from components.dashboard import Window


class DashButton(Static):
    def render_line(self, y: int) -> Strip:
        """Render a line of the app drawer icon."""
        app_drawer_icon = [
            " • • • ",
            " • • • "
        ]

        if y >= len(app_drawer_icon):
            return Strip.blank(self.size.width)

        line = app_drawer_icon[y]
        segment = Segment(line, Style(color="rgb(233, 84, 32)"))
        return Strip([segment], len(line))

    def on_click(self):
        try:
            window = self.app.query_one("#dashboard_window")
            if window:
                return
        except Exception as e:
            pass
        self.app.mount(Window(0, 0, 50, 20, "", "vOS Dashboard", "dashboard_window"))

class Dash(Static):

    def compose(self) -> ComposeResult:
        yield DashButton("\n", classes="dashapp")

    def is_mouse_over_dash(
        self,
        mouse_x, mouse_y
        ):
        widget = self.region
        return (
             widget.x <= mouse_x <= widget.x + widget.width
             and
             widget.y <= mouse_y <= widget.y + widget.height
             )
    def dash_animation(self, reveal: bool):
        if reveal:
            self.styles.animate("opacity", value=100.0, duration=1.5)
            self.dash_timer = 0
            self.update_clock()
            self.dash_clock = self.set_interval(6, self.update_clock)
        else:
            self.styles.animate("opacity", value=0.0, duration=0.5)
            self.dash_clock.pause()

    @staticmethod
    def get_dash_opacity(self):
        return self.opacity

    @on(events.MouseEvent)
    def dash_thrigger(self, event: events.MouseEvent) -> None:
        dash_loc = self.region
        timer = 0
        if self.is_mouse_over_dash(
            event.x, event.y
            ):
            if self.opacity == 0.0:
                self.dash_animation(True)
            else:
                self.dash_animation(False)

        else:
            if self.opacity == 100.0:
                self.dash_animation(False)

    @work(thread=True)
    def update_clock(self) -> None:
        if self.dash_timer == 3:
            self.dash_animation(False)
            self.dash_timer = 0
        else:
            self.dash_timer += 1
