from textual.app import App, ComposeResult
from textual.widgets import Input, TextArea
from textual.screen import Screen
from textual import events, on, work
from textual.containers import Vertical
import socket
import threading


class IRCScreen(Screen):
    nickname = ""
    def compose(self) -> ComposeResult:
        self.text_area = TextArea(id="ircoutput")
        self.text_area.read_only = True
        self.text_area.cursor_blink = False
        self.text_area.theme = "vscode_dark"
        self.input = Input(placeholder="admin: ", id="ircinput")
        with Vertical():
            yield self.text_area
            yield self.input


    async def on_mount(self):
        self.start_client("192.168.254.1", 67, "admin")

    async def receive_messages(self, client_socket):
        try:
            message = self.client_socket.recv(4096).decode('utf-8')
            if message:
               self.call_from_thread(self.text_area.insert, f"{message}\n")
            else:
                pass
        except Exception as e:
             self.call_from_thread(self.text_area.insert, f"Error receiving message: {e}")


    @work(exclusive=True)
    async def start_client(self, server_ip, server_port, nickname):
        self.nickname = nickname
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((server_ip, server_port))
        except Exception as e:
            self.text_area.insert(f"Error connecting to server: {e}")
            return

        receive_thread = threading.Thread(target=self.receive_messages, args=(self.client_socket,))
        receive_thread.daemon = True
        receive_thread.start()

    async def on_input_submitted(self, event: Input.Submitted):
        message = event.value
        if message:
            if message == '/quit':
#                self.client_socket.send(f"{self.nickname} has left the chat.".encode('utf-8'))
#                self.client_socket.close()
                self.app.push_screen("TerminalScreen")
            else:
                self.client_socket.send(f"{self.nickname}: {message}".encode('utf-8'))
                self.text_area.insert(f"Me: {message}\n")
                self.input.value = ""



