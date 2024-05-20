from textual.app import App, ComposeResult
from textual.screen import Screen
from textual import on, events, work
from Settings import SettingsScreen
from Dashboard import DashScreen
from Terminal import TerminalScreen
from Login import LoginScreen
from components.dash  import Dash
from components.topbar import Clock, TopBar
from components.background_gradient import ScreenSaver
#



class DesktopBase(Screen):
    def compose(self) -> ComposeResult:
        self.dash = Dash(id="dash", classes="DashClass")
        yield self.dash
        yield TopBar(id="topbar")



class Desktop(App):
    CSS_PATH = "Desktop.tcss"
    SCREENS = {
        "DesktopBase": DesktopBase(),
        "DashScreen": DashScreen(),
        "SettingsScreen": SettingsScreen(),
        "ScreenSaver": ScreenSaver(),
        "TerminalScreen": TerminalScreen(),
        "LoginScreen": LoginScreen()
     }

    @work
    async def on_mount(self) -> None:
        await self.push_screen_wait("LoginScreen")

if __name__ == "__main__":
    app = Desktop()
    app.run()
