from textual.app import App, ComposeResult
from textual.screen import Screen
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
    def compose(self) -> ComposeResult:
        self.dash = Dash(id="dash", classes="DashClass")
        yield self.dash
        yield TopBar(id="topbar")

    def on_click(self):
        try:
            window = self.query_one("#dashboard_window")
#            if window.styles.opacity != 0.0:
#                window.styles.animate("opacity", value=0.0, duration=1/6, on_complete=window.remove)
        except:
            pass

class Desktop(App):
    CSS_PATH = "Desktop.tcss"
    SCREENS = {
        "DesktopBase": DesktopBase(),
        "DashScreen": DashScreen(),
        "SettingsScreen": SettingsScreen(),
        "ScreenSaver": ScreenSaver(),
        "TerminalScreen": TerminalScreen(),
        "LoginScreen": LoginScreen(),
        "QChat": IRCScreen()
     }

    @work
    async def on_mount(self) -> None:
        await self.push_screen_wait("LoginScreen")

if __name__ == "__main__":
    app = Desktop()
    app.run()
