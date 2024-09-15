"""TCP Client for JR Touch Panel."""
import asyncio

class JRTouchPanelTCPClient:
    """TCP client for communicating with the JR Touch Panel."""

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._reader = None
        self._writer = None

    async def connect(self):
        """Establish a connection to the JR Touch Panel."""
        self._reader, self._writer = await asyncio.open_connection(self._host, self._port)

    async def set_switch_state(self, device_id: int, state: bool):
        """Send a command to set the switch state."""
        command = f"SET SWITCH {device_id} {'ON' if state else 'OFF'}"
        self._writer.write(command.encode())
        await self._writer.drain()

    async def set_fan_speed(self, device_id: int, speed: int):
        """Set the fan speed."""
        command = f"SET FAN {device_id} SPEED {speed}"
        self._writer.write(command.encode())
        await self._writer.drain()

    async def set_dimmer_brightness(self, device_id: int, brightness: int):
        """Set the dimmer brightness."""
        command = f"SET DIMMER {device_id} BRIGHTNESS {brightness}"
        self._writer.write(command.encode())
        await self._writer.drain()

    async def set_cover_position(self, device_id: int, position: int):
        """Set the cover position."""
        command = f"SET COVER {device_id} POSITION {position}"
        self._writer.write(command.encode())
        await self._writer.drain()
    
    async def disconnect(self):
        """Close the connection."""
        self._writer.close()
        await self._writer.wait_closed()
      
