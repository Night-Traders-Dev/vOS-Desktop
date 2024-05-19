from textual.app import App, ComposeResult
from textual.color import Color
from textual.widgets import Static, LoadingIndicator, Input
from textual.containers import Grid
from textual.geometry import Region
from textual.screen import Screen, ModalScreen
from textual import on, events, work
from datetime import datetime


class LoginPrompt(Input):
    username = ""
    password = ""


    def __init__(
        self,
        value="",
        id=None,
        placeholder="",
        password=False,
    ):
        super().__init__()
        self.placeholder = "Username"
    @on(Input.Submitted)
    def collect_and_send(self, event: Input.Submitted):
        global username, password
        if not self.password:
            username = event.value
            self.password = True
            self.placeholder = "Password"
            self.value = ""
        else:
            password = event.value
            username = ""
            password = ""
            self.value = ""
            self.password = False
            self.placeholder = "Username"
            self.app.push_screen("DesktopBase")



class LoginScreen(Screen):


    def compose(self) -> ComposeResult:
        yield Static(id="topbar")
        yield Static("", id="clock")
        yield LoginPrompt(id="userprompt")


# Clock Method
    @on(events.Mount)
    def clock_timer(self) -> None:
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one("#clock", Static).update(f"{clock:%T}")
    # End Clock
