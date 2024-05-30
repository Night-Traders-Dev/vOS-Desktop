from textual.app import ComposeResult, RenderResult
from textual import on, events
from textual.widgets import Static
from components.battery_android_bar import BatteryBar
from components.os_check import EnvironmentChecker as os_check
from datetime import datetime

class Clock(Static):

    # Clock Method
    @on(events.Mount)
    def clock_timer(self) -> None:
        self.render()
        self.set_interval(1, self.update_clock)

    def render(self) -> RenderResult:
            clock = datetime.now().time()
            return (f"{clock:%T}")

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.update(f"{clock:%T}")

class TopBar(Static):
    def compose(self) -> ComposeResult:
        yield Clock(id="clock")
        if os_check.is_android() and os_check.is_termux() and os_check.is_proot():
            yield BatteryBar()
