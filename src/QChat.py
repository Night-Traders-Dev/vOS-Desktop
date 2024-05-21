import asyncio
from textual.app import App, ComposeResult
from textual.widgets import Input, TextArea
from textual.screen import Screen
from textual.containers import Vertical
from textual import events, on

class IRCScreen(Screen):
    nickname = "admin"

    def compose(self) -> ComposeResult:
        self.text_area = TextArea(id="ircoutput")
        self.text_area.read_only = True
        self.text_area.cursor_blink = False
        self.text_area.theme = "vscode_dark"
        self.input = Input(placeholder=f"{self.nickname}: ", id="ircinput")
        with Vertical():
            yield self.text_area
            yield self.input

    async def on_mount(self):
        self.message_history = []
        await self.start_client("192.168.254.1", 8001, self.nickname)

    async def handle_server(self, reader):
        try:
            while True:
                data = await reader.read(100)
                if not data:
                    break
                message = data.decode().strip()
                self.message_history.append(message)
                await self.update_messages()
        except asyncio.CancelledError:
            pass

    async def send_message(self, writer, message):
        writer.write(f"{self.nickname}: {message}\n".encode())
        await writer.drain()
        self.message_history.append(f"Me: {message}")
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
        if message:
            await self.send_message(self.writer, message)
            self.input.value = ""

    async def on_unmount(self):
        self.receive_task.cancel()
        await self.writer.wait_closed()

