from textual.app import App, ComposeResult
from components.topbar import Clock, TopBar
from textual.widgets import Input, Label, Static
from textual.screen import Screen
from textual import on, events
from components.notif import Window as Notif
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
        x, y = self.screen.size
        if not self.password:
            username = event.value
            if username != "":
                self.password = True
                self.placeholder = "Password"
                self.value = ""
            else:
                self.parent.mount(Notif((x - 22), (y - 6), 0, 0, "Username Required", "vOS Notification"))
        else:
            password = event.value
            if password != "":
                if self.auth():
                    self.app.push_screen("DesktopBase")
                else:
                    self.parent.mount(Notif((x - 22), (y - 6), 0, 0, "Account Not Found", "vOS Notification"))
                    username = ""
                    password = ""
                    self.value = ""
                    self.password = False
                    self.placeholder = "Username"
            else:
                self.parent.mount(Notif((x - 22), (y - 6), 0, 0, "Password Required", "vOS Notification"))

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
    AUTO_FOCUS = "#userprompt"


    def compose(self) -> ComposeResult:
        yield TopBar(id="topbar")
        yield Label("vOS Login", id="LoginLabel")
        self.loginprompt = LoginPrompt(id="userprompt")
        yield self.loginprompt
        self.loginprompt.focus()


