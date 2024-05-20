from textual.app import App, ComposeResult
from components.topbar import Clock, TopBar
from textual.widgets import Input, Label, Static
from textual.screen import Screen
from textual import on, events
#from vapi.vapi import passwordtools_instance
#from vapi.vapi import fs_instance

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
                if self.auth():
                    self.notify(f"{username} logged in.", title="vOS Notification")
                    self.app.push_screen("DesktopBase")
                else:
                    self.notify("Account Not Found", title="vOS Notification", severity="warning", timeout = 1.25)
                    username = ""
                    password = ""
                    self.value = ""
                    self.password = False
                    self.placeholder = "Username"
            else:
                self.notify("Password Required", title="vOS Notification", severity="warning", timeout = 1.25)

    def auth(self):
        if username == "admin" and password == "admin":
            return True
        else:
            return False
#        self.fs = fs_instance()
#        elf.passwordtools = passwordtools_instance()
#        self.passwordtools.check_passwd_file(self.fs)
#        login = self.passwordtools.authenticate(username, password)
#        if login:
#            self.dismiss(True)
#        else:
#            self.mount(Label("Account not found!"))


class LoginScreen(Screen):


    def compose(self) -> ComposeResult:
        yield TopBar(id="topbar")
        yield Label("vOS Login", id="LoginLabel")
        yield LoginPrompt(id="userprompt")


