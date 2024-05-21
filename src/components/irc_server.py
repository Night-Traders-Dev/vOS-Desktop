import asyncio
from datetime import datetime

class IRCServerProtocol(asyncio.Protocol):
    clients = []

    def __init__(self):
        self.transport = None
        self.nickname = None

    def connection_made(self, transport):
        self.transport = transport
        self.peername = transport.get_extra_info('peername')
        self.transport.write(b"Welcome to the IRC server! Please set your nickname with /nick <your_nickname>.\n")
        IRCServerProtocol.clients.append(self)
        print(f"Connection from {self.peername}")

    def data_received(self, data):
        message = data.decode().strip()
        if message.startswith("/nick "):
            self.nickname = message.split(" ", 1)[1]
            self.transport.write(f"Nickname set to {self.nickname}\n".encode())
        else:
            if self.nickname:
                timestamp = datetime.now().strftime("%H:%M:%S")
                formatted_message = f"[{timestamp}] {self.nickname}: {message}"
                self.broadcast_message(formatted_message)
            else:
                self.transport.write(b"Please set your nickname with /nick <your_nickname> before sending messages.\n")

    def connection_lost(self, exc):
        print(f"Client {self.peername} disconnected")
        IRCServerProtocol.clients.remove(self)
        if exc:
            print(f"Connection lost due to error: {exc}")

    def broadcast_message(self, message):
        for client in IRCServerProtocol.clients:
            client.transport.write(f"{message}\n".encode())

async def main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: IRCServerProtocol(),
        '127.0.0.1', 67
    )

    async with server:
        print(f"Server started at {datetime.now()}")
        await server.serve_forever()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Server error: {e}")
