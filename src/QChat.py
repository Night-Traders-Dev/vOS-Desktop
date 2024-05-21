from textual.app import App, ComposeResult
from textual.widgets import Input, TextArea
from textual.screen import Screen
from textual import events, on
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

    def on_mount(self):
        self.start_client("127.0.0.1", 6667, "admin")

    def receive_messages(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024).decode('utf-8')
                if message:
                    self.call_from_thread(self.update_text_area, message)
                else:
                    break
            except Exception as e:
                self.call_from_thread(self.update_text_area, f"Error receiving message: {e}")
                break

    def update_text_area(self, message: str):
        self.text_area.append(f"{message}\n")

    def start_client(self, server_ip, server_port, nickname):
        self.nickname = nickname
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((server_ip, server_port))
        except Exception as e:
            self.update_text_area(f"Error connecting to server: {e}")
            return

        receive_thread = threading.Thread(target=self.receive_messages, args=(self.client_socket,))
        receive_thread.daemon = True
        receive_thread.start()

    def on_input_submitted(self, event: Input.Submitted):
        message = event.value
        if message:
            if message == '/quit':
                self.client_socket.send(f"{self.nickname} has left the chat.".encode('utf-8'))
                self.client_socket.close()
                self.app.exit()
            else:
                self.client_socket.send(f"{self.nickname}: {message}".encode('utf-8'))
                self.input.value = ""

    @on(Input.Submitted)
    def handle_input(self, event: Input.Submitted) -> None:
        self.on_input_submitted(event)


