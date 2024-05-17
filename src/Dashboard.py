from textual.app import ComposeResult
from textual.color import Color
from textual.widgets import Static, Label, ListItem, ListView
from textual.containers import Grid
from textual.geometry import Region
from textual.screen import Screen, ModalScreen
from textual import on, events, work
from datetime import datetime



class DashScreen(ModalScreen[str]):

    CSS_PATH = "Desktop.tcss"
    def compose(self) -> ComposeResult:
        yield Static(id="topbar")
        yield Static("", id="clock")
        yield Static("App One", classes="box")
        yield Static("App Two", classes="box")
        yield Static("App Three", classes="box")
        yield Static("App Four", classes="box")
        yield Static("App Five", classes="box")
        yield Static("App Six", classes="box")
        yield Static("App Seven", classes="box")
        yield Static("App Eight", classes="box")
        yield Static("App Nine", classes="box")

    # Clock Method
    @on(events.Mount)
    def clock_timer(self) -> None:
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self) -> None:
        clock = datetime.now().time()
        self.query_one("#clock", Static).update(f"{clock:%T}")
    # End Clock
    @on(events.MouseEvent)
    def go_back(self):
        self.app.push_screen("SettingsScreen")
#        self.dismiss("App Name")
