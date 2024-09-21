from textual.app import App, ComposeResult
from textual.events import Click
from textual.geometry import Region
from textual.screen import Screen
from textual.widgets import LoadingIndicator
from textual import on, events, work
from Settings import SettingsScreen
from Dashboard import DashScreen
from Terminal import TerminalScreen
from Login import LoginScreen
from QChat import IRCScreen
from components.dash  import Dash
from components.topbar import Clock, TopBar
from components.background_gradient import ScreenSaver



class DesktopBase(Screen):

    def close_dashboard(self) -> None:
        try:
            window = self.query_one("#dashboard_window")
            window.styles.animate("opacity", value=0.0, duration=1/6, on_complete=window.remove)
        except:
            pass

    def on_click(self, event: Click) -> None:
        click_x = event.x
        click_y = event.y

        try:
            window = self.query_one("#dashboard_window")

            widget_x, widget_y, widget_width, widget_height = window.region

            if widget_width == 50 and widget_height == 20:
                if (click_x < widget_x or
                    click_x > (widget_x + widget_width) or
                    click_y < widget_y or
                    click_y > (widget_y + widget_height)):
                    self.close_dashboard()
        except:
            pass

    def key_space(self) -> None:
        self.close_dashboard()

    def compose(self) -> ComposeResult:
        self.dash = Dash(id="dash", classes="DashClass")
        yield self.dash
        yield TopBar(id="topbar")

class Desktop(App):
    CSS_PATH = "Desktop.tcss"
    SCREENS = {
        "DesktopBase": DesktopBase,
        "DashScreen": DashScreen,
        "SettingsScreen": SettingsScreen,
        "ScreenSaver": ScreenSaver,
        "TerminalScreen": TerminalScreen,
        "LoginScreen": LoginScreen,
        "QChat": IRCScreen
     }

    def compose(self) -> ComposeResult:
        yield DesktopBase(id="DesktopBase")

    @work(exclusive=True)
    async def on_mount(self) -> None:
        self.push_screen("LoginScreen")

if __name__ == "__main__":
    app = Desktop()
    app.run()
