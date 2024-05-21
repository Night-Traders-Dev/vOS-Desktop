from textual.app import ComposeResult
from textual.color import Color
from textual.widgets import Static, Label, ListItem, ListView
from textual.containers import Grid
from textual.geometry import Region
from textual.screen import Screen, ModalScreen
from textual import on, events, work
from datetime import datetime
from rich.segment import Segment
from rich.style import Style
from textual.strip import Strip
from components.topbar import Clock, TopBar

class SettingsApp(Static):
    def render_line(self, y: int) -> Strip:
        """Render a line of the settings icon."""
        settings_icon = [
            "  ⚙⚙⚙  ",
            " ⚙⚙⚙⚙⚙ ",
            "⚙⚙⚙⚙⚙⚙⚙",
            " ⚙⚙⚙⚙⚙ ",
            "  ⚙⚙⚙  ",
            "Settings"
        ]

        if y >= len(settings_icon):
            return Strip.blank(self.size.width)

        line = settings_icon[y]
        segment = Segment(line, Style(color="yellow", bold=True))
        return Strip([segment], len(line))

    def on_click(self):
        self.app.push_screen("SettingsScreen")

class TerminalApp(Static):
    def render_line(self, y: int) -> Strip:
        """Render a line of the terminal icon."""
        terminal_icon = [
            " _______ ",
            "|       |",
            "|   >_  |",
            "|_______|",
            "Terminal "
        ]

        if y >= len(terminal_icon):
            return Strip.blank(self.size.width)

        line = terminal_icon[y]
        segment = Segment(line, Style(color="green", bold=True))
        return Strip([segment], len(line))

    def on_click(self):
        self.app.push_screen("TerminalScreen")


class RandomApp(Static):
    def on_click(self):
        self.app.push_screen("DesktopBase")

class DashScreen(ModalScreen[str]):

    CSS_PATH = "Desktop.tcss"
    def compose(self) -> ComposeResult:
        yield TopBar(id="topbar")
        yield TerminalApp("Terminal", id="terminal", classes="box")
        yield SettingsApp("Settings", id="settings",  classes="box")
        yield RandomApp("App Three", classes="box")
        yield RandomApp("App Four", classes="box")
        yield RandomApp("App Five", classes="box")
        yield RandomApp("App Six", classes="box")
        yield RandomApp("App Seven", classes="box")
        yield RandomApp("App Eight", classes="box")
        yield RandomApp("App Nine", classes="box")

