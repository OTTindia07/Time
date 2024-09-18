from homeassistant.components.cover import CoverEntity
from .tcp_client import JRTouchPanelTCPClient

class JRTouchPanelCover(CoverEntity):
    """Representation of a motorized cover controlled by the JR Touch Panel."""

    def __init__(self, client: JRTouchPanelTCPClient, device_id: int, name: str):
        self.client = client
        self.device_id = device_id
        self._name = name
        self._position = 0

    @property
    def name(self):
        return self._name

    @property
    def current_cover_position(self):
        return self._position

    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        await self.client.send({"device_id": self.device_id, "action": "open"})
        self._position = 100
        self.async_write_ha_state()

    async def async_close_cover(self, **kwargs):
        """Close the cover."""
        await self.client.send({"device_id": self.device_id, "action": "close"})
        self._position = 0
        self.async_write_ha_state()

    async def async_set_cover_position(self, position, **kwargs):
        """Set the cover to a specific position."""
        await self.client.send({"device_id": self.device_id, "position": position})
        self._position = position
        self.async_write_ha_state()
