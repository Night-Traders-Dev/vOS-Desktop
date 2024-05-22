from rich.segment import Segment
from rich.style import Style
from textual.strip import Strip
from textual.app import App, ComposeResult, RenderResult
from textual.widgets import Static
from textual.containers import Grid
from textual.geometry import Region
from textual.screen import Screen
from textual import on, events, work



class Gesture(Static):

    # MouseMove Alternative
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


