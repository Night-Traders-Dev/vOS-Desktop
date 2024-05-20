from textual.app import ComposeResult, RenderResult
from textual import on, events
from textual.widgets import Static
from datetime import datetime

class Clock(Static):
    idle_timer = 0

    # Clock Method
    @on(events.Mount)
    def clock_timer(self) -> None:
        self.render()
        self.auto_refresh = 1

    def render(self) -> RenderResult:
            clock = datetime.now().time()
            return (f"{clock:%T}")

#        global idle_timer
#        if idle_timer == 60:
#            idle_timer = 0
#            self.app.push_screen("ScreenSaver")
#        else:
#            idle_timer += 1
    # End Clock

class TopBar(Static):
    def compose(self) -> ComposeResult:
        yield Clock(id="clock")
