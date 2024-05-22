import asyncio
import random
from textual.app import App, ComposeResult
from textual.widgets import Input, TextArea
from textual.screen import Screen
from textual.containers import Vertical
from textual import events, on

class IRCScreen(Screen):
    AUTO_FOCUS = "#ircinput"

    nickname = "user" +  str(random.randint(0, 999999))
    channels = ["#qchat", "#market", "#help"]
    current_channel = "#qchat"


    def compose(self) -> ComposeResult:
        self.text_area = TextArea(id="ircoutput")
        self.text_area.read_only = True
        self.text_area.cursor_blink = False
        self.text_area.theme = "vscode_dark"
        self.text_area.border_title = "QChat"
        self.text_area.border_subtitle = f"Channel: {self.current_channel}"
        self.input = Input(placeholder=f"{self.nickname}: ", id="ircinput")
        with Vertical():
            yield self.text_area
            yield self.input

    async def on_mount(self):
        self.message_history = []
        self.current_channel = '#qchat'
        await self.start_client("71.29.176.68", 8001, self.nickname)

    async def handle_server(self, reader):
        try:
            while True:
                data = await reader.read(100)
                if not data:
                    break
                message = data.decode().strip()
                if "(private)" in message and message.split()[1] != self.nickname:
                    self.notify("Private Message Received", title="vOS Notification")
                self.message_history.append(message)
                await self.update_messages()
        except asyncio.CancelledError:
            pass

    async def send_message(self, writer, message):
        writer.write(f"{message}\n".encode())
        await writer.drain()
        await self.update_messages()

    async def start_client(self, server_ip, server_port, nickname):
        self.reader, self.writer = await asyncio.open_connection(server_ip, server_port)
        self.writer.write(f"/nick {nickname}\n".encode())
        await self.writer.drain()

        self.receive_task = asyncio.create_task(self.handle_server(self.reader))

    async def update_messages(self):
        self.text_area.clear()
        for message in self.message_history:
            self.text_area.insert(f"{message}\n")

    async def on_input_submitted(self, event: Input.Submitted):
        message = event.value
        send_message = True
        if message == '/quit':
            await self.quit_client()
        elif message:
            if message.startswith('/nick'):
                self.input.placeholder = message.split(" ", 1)[1]
            elif message.startswith('/join'):
                if message.split(" ", 1)[1] not in self.channels:
                    self.text_area.insert(f'{message.split(" ", 1)[1]} not a channel\n')
                    send_message = False
                else:
                    self.current_channel = message.split(" ", 1)[1]
                    self.text_area.border_subtitle = f"Channel: {self.current_channel}"
            if send_message:
                await self.send_message(self.writer, message)
                self.input.value = ""


    async def quit_client(self):
        self.client_running = False
        self.writer.write(f"{self.nickname} has left the chat.\n".encode())
        await self.writer.drain()

        # Close the writer and reader
        self.writer.close()
        try:
            await asyncio.wait_for(self.writer.wait_closed(), timeout=3.0)
        except asyncio.TimeoutError:
            pass

        self.receive_task.cancel()
        try:
            await self.receive_task
        except asyncio.CancelledError:
            pass

        self.app.push_screen("TerminalScreen")

    async def on_unmount(self):
        if hasattr(self, 'receive_task'):
            self.receive_task.cancel()
            try:
                await self.receive_task
            except asyncio.CancelledError:
                pass

        if hasattr(self, 'writer'):
            self.writer.close()
            try:
                await asyncio.wait_for(self.writer.wait_closed(), timeout=3.0)
            except asyncio.TimeoutError:
                pass


