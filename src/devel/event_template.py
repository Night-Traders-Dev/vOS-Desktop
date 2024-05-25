from textual import on
from textual.app import App, ComposeResult
from textual.css.query import NoMatches
from textual.events import *
from textual.widgets import Log

class EventLog(App[None]):
    # Define the set of event types to capture
    CAPTURED_EVENTS = {
             Resize, MouseDown,
             MouseUp, Click,
             Blur, Focus,
             Enter, Leave,
             InputEvent, Key,
     }

    def compose(self) -> ComposeResult:
        yield Log()

    @on(Event)
    def log_event(self, event: Event) -> None:
        # Check if the event type is in the whitelist
        if type(event) in self.CAPTURED_EVENTS:
            try:
                self.query_one(Log).write_line(f"{event!r}")
            except NoMatches:
                pass

if __name__ == "__main__":
    EventLog().run()
