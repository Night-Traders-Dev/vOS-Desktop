from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.css.query import NoMatches
from textual.events import *
from textual.message import *
from textual.widgets import Log
from datetime import datetime

class EventLog(App[None]):

    DEFAULT_CSS = """
        App {
            align: left top;
        }
        Log {
        content-align: left top;
        layout: vertical;
        text-align: left;
        background: rgba(119, 41, 83, 100.0);
        height: 100%;
        width: 100%;
        }
        """
    CAPTURED_EVENTS = {
             Resize, MouseDown,
             MouseUp, Click,
             Blur, Focus,
             Enter, Leave,
             InputEvent, Key,
     }

    def compose(self) -> ComposeResult:
        yield Log()
#        self.debug.box_sizing = "content-box"

    @on(Message)
    def log_message(self, message: Message) -> None:
        if f"{message!r}" != "Idle()":
            try:
                self.query_one(Log).write_line(f"{datetime.now()} Message: {message!r}\n")
            except NoMatches:
                pass
    @on(Event)
    def log_event(self, event: Event) -> None:
        if type(event) in self.CAPTURED_EVENTS:
            try:
                self.query_one(Log).write_line(f"{datetime.now()} Event: {event!r}\n")
            except NoMatches:
                pass

if __name__ == "__main__":
    EventLog().run()
