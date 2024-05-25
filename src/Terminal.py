from textual import events, on
from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import TextArea
from components.topbar import Clock, TopBar
#from vapi.vapi import CommandParse

class Terminal(TextArea):

    def on_mount(self):
        self.show_line_numbers = False
        self.insert("$ ")

    def _on_key(self, event: events.Key) -> None:
        curline, currow = self.get_cursor_line_start_location()
        if currow == 1:
            self.undo()
        if event.key == "enter":
            curline, currow = self.get_cursor_line_start_location()
            command = self.get_line(curline)
            command = str(command).strip("$ ")
            self.insert("\n" + command + "\n$ ")
            event.prevent_default()
            self.handle_command(command.lower())

    def handle_command(self, command: str):
        # Dictionary mapping commands to their handler functions
        command_handlers = {
            "exit": self.handle_exit,
            "shutdown": self.handle_shutdown,
            "qchat": self.handle_qchat,
            "screensaver": self.handle_screensaver
        }

        # Get the handler function from the dictionary
        handler = command_handlers.get(command, self.handle_unknown_command)
        # Call the handler function
        handler()

    def handle_exit(self):
        self.clear()
        self.insert("\nexit\n$ ")
        self.app.push_screen("DesktopBase")

    def handle_shutdown(self):
        self.app.exit()

    def handle_qchat(self):
        self.app.push_screen("QChat")

    def handle_screensaver(self):
        self.app.push_screen("ScreenSaver")

    def handle_unknown_command(self):
        # Handle unknown command (you can customize this)
        self.insert("\nUnknown command\n$ ")

class TerminalScreen(Screen):

    CSS_PATH = "Desktop.tcss"

    def compose(self) -> ComposeResult:
        yield TopBar(id="topbar")
        yield Terminal.code_editor(language="python")
