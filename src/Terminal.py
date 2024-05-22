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
            if command == "exit":
                self.clear()
                self.insert("\n" + command + "\n$ ")
                self.app.push_screen("DesktopBase")
            elif command == "shutdown":
                self.app.exit()
            elif command.lower() == "qchat":
                self.app.push_screen("QChat")
            else:
                pass



class TerminalScreen(Screen):

    CSS_PATH = "Desktop.tcss"

    def compose(self) -> ComposeResult:
        yield TopBar(id="topbar")
        yield Terminal.code_editor(language="python")



