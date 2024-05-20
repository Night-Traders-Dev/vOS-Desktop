from textual.app import App, ComposeResult
from components.topbar import Clock, TopBar
from textual.widgets import Input, Label, Static
from textual.screen import Screen
from textual import on, events


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
            if username != "":
                self.password = True
                self.placeholder = "Password"
                self.value = ""
            else:
                self.notify("Username Required", title="vOS Notification", severity="warning", timeout = 1.25)
        else:
            password = event.value
            if password != "":
                self.notify(f"{username} logged in.", title="vOS Notification")
                username = ""
                password = ""
                self.value = ""
                self.password = False
                self.placeholder = "Username"
                self.app.push_screen("DesktopBase")
            else:
                self.notify("Password Required", title="vOS Notification", severity="warning", timeout = 1.25)


class LoginScreen(Screen):


    def compose(self) -> ComposeResult:
        yield TopBar(id="topbar")
        yield Label("vOS Login", id="LoginLabel")
        yield LoginPrompt(id="userprompt")


