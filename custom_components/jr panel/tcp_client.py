import asyncio
import socket
import logging

_LOGGER = logging.getLogger(__name__)

class JRTouchPanelTCPClient:
    """Client class to handle communication with the JR Touch Panel."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.client = None

    async def connect(self):
        """Establish a connection to the JR Touch Panel."""
        loop = asyncio.get_event_loop()
        self.client = await loop.run_in_executor(None, lambda: socket.create_connection((self.host, self.port)))
        _LOGGER.info(f"Connected to JR Touch Panel at {self.host}:{self.port}")

    async def send_command(self, device_id: int, value: int):
        """Send a command to the JR Touch Panel."""
        command = f'{{"set":{{"dp_id":{device_id},"value":{value}}}}}'
        _LOGGER.debug(f"Sending command: {command}")
        self.client.sendall(command.encode())

    async def set_switch_state(self, device_id: int, state: bool):
        """Set the state of a switch."""
        value = 1 if state else 0
        await self.send_command(device_id, value)

    async def set_fan_speed(self, device_id: int, speed: int):
        """Set the speed of a fan."""
        await self.send_command(device_id, speed)

    async def set_dimmer_brightness(self, device_id: int, brightness: int):
        """Set the brightness of a dimmer."""
        await self.send_command(device_id, brightness)

    async def set_cover_position(self, device_id: int, position: int):
        """Set the position of a cover."""
        await self.send_command(device_id, position)
