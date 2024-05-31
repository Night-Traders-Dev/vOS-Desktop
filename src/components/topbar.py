from textual.app import ComposeResult, RenderResult
from textual import on, events, work
from textual.widgets import Static
from components.os_check import EnvironmentChecker as os_check
from components.battery_bar import BatteryBar
from datetime import datetime

class Clock(Static):

    @on(events.Mount)
    def clock_timer(self) -> None:
        self.render()
        self.set_interval(1, self.update_clock)

    def render(self) -> RenderResult:
            clock = datetime.now().time()
            return (f"{clock:%T}")

    @work(thread=True)
    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.update(f"{clock:%T}")

class TopBar(Static):
    def compose(self) -> ComposeResult:
        yield Clock(id="clock")
        yield BatteryBar()
