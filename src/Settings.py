from textual.app import ComposeResult, RenderResult
from textual.color import Color
from textual.widgets import Static, Label, ListItem, ListView, Rule
from textual.containers import Grid
from textual.geometry import Region
from textual.message import Message
from textual.screen import Screen, ModalScreen
from textual import on, events, work
from datetime import datetime



class SettingsScreen(Screen):

    class SettingButton(Static):

        def __init__(self, setting: str) -> None:
            self.setting = setting
            super().__init__()

        def render(self) -> RenderResult:
            if self.setting == "account":
                name = "Account"
            elif self.setting == "display":
                name = "Display"
            elif self.setting == "qseconfig":
                name = "QSE Config"
            elif self.setting == "back":
                name = "Back to Desktop"
            else:
                name = "Default Stub"
            return str(name)


        def on_click(self) -> None:
            if self.setting == "back":
                self.app.push_screen("DesktopBase")
            else:
                self.notify(f"{self.setting} pressed", title="vOS Notification")

    CSS_PATH = "Desktop.tcss"

    def compose(self) -> ComposeResult:
        yield Static(id="topbarsettings")
        yield Static("", id="clocksettings")
        yield ListView(
            ListItem(self.SettingButton("account")),
            ListItem(self.SettingButton("display")),
            ListItem(self.SettingButton("qseconfig")),
            ListItem(self.SettingButton("back")),id="sidebar"
        )


