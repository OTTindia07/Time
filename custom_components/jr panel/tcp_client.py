import asyncio
import json

class JRTouchPanelTCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.reader = None
        self.writer = None

    async def connect(self):
        """Establish a connection to the JR Touch Panel."""
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    async def send(self, command):
        """Send a command to the JR Touch Panel."""
        self.writer.write(json.dumps(command).encode())
        await self.writer.drain()

    async def receive(self):
        """Receive a response from the JR Touch Panel."""
        data = await self.reader.read(100)
        return json.loads(data.decode())

    async def disconnect(self):
        """Close the connection to the JR Touch Panel."""
        if self.writer:
            self.writer.close()
            await self.writer.wait_closed()
