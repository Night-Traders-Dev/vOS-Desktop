from textual.app import App, ComposeResult
from textual.color import Color
from textual.widgets import Static, LoadingIndicator
from textual.containers import Grid
from textual.geometry import Region
from textual.screen import Screen, ModalScreen
from textual import on, events, work
from datetime import datetime
from Settings import SettingsScreen
from Dashboard import DashScreen
from Terminal import TerminalScreen
from components.background_gradient import ScreenSaver


class DashButton(Static):
    def on_click(self):
        self.app.push_screen("DashScreen")


class Dash(Static):
    def compose(self) -> ComposeResult:
        yield DashButton("Dash\nboard", classes="dashapp")



class DesktopBase(Screen):

    def compose(self) -> ComposeResult:
        self.dash = Dash(id="dash", classes="DashClass")
        yield self.dash
        yield Static(id="topbar")
        yield Static("", id="clock")


    # Clock Method
    @on(events.Mount)
    def clock_timer(self) -> None:
        self.idle_timer = 0
        self.dash_open = False
        self.dash_timer = 0
        self.update_clock()
        self.set_interval(1, self.update_clock)

    def update_clock(self) -> None:
        if self.dash_open:
           if self.dash_timer != 3:
              self.dash_timer += 1
           else:
              self.dash_animation(False)
        if self.idle_timer == 60:
            self.idle_timer = 0
            self.app.push_screen("ScreenSaver")
        else:
            self.idle_timer += 1
        clock = datetime.now().time()
        self.query_one("#clock", Static).update(f"{clock:%T}")
    # End Clock

    # MouseMove Alternative
    def is_mouse_over_widget(
        self, widget_x, widget_y, widget_width, widget_height,
        mouse_x, mouse_y,
        screen_width, screen_height
        ):
        return widget_x <= mouse_x <= widget_x + widget_width and widget_y <= mouse_y <= widget_y + widget_height

    def dash_animation(self, reveal: bool):
        if reveal:
            self.dash.styles.animate("opacity", value=100.0, duration=1.5)
            self.dash_open = True
        else:
            self.dash.styles.animate("opacity", value=0.0, duration=0.5)
            self.dash_open = False
            self.dash_timer = 0


    # Dash Reveal Trigger
    @on(events.MouseEvent)
    def dash_thrigger(self, event: events.MouseEvent) -> None:
        self.idle_timer = 0
        dash_loc = self.dash.region
        term_height = 24
        term_width = 80
        if self.is_mouse_over_widget(
            dash_loc.x, dash_loc.y, dash_loc.width, dash_loc.height,
            event.x, event.y,
            term_width, term_height
            ):
            if self.dash.opacity == 0.0:
                self.dash_animation(True)
            else:
                pass

        else:
            self.dash_animation(False)
    # End Dash Reveal



class Desktop(App):
    CSS_PATH = "Desktop.tcss"
    SCREENS = {"DesktopBase": DesktopBase(), "DashScreen": DashScreen(), "SettingsScreen": SettingsScreen(), "ScreenSaver": ScreenSaver(), "TerminalScreen": TerminalScreen()}

    def on_load(self) -> ComposeResult:
        yield LoadingIndicator()
        self.set_timer(10)
    @work
    async def on_mount(self) -> None:
        await self.push_screen_wait("DesktopBase")

if __name__ == "__main__":
    app = Desktop()
    app.run()
