from homeassistant.components.cover import CoverEntity
from .tcp_client import JRTouchPanelTCPClient

class JRTouchPanelCover(CoverEntity):
    """Representation of a JR Touch Panel cover."""

    def __init__(self, client: JRTouchPanelTCPClient, device_id: int, name: str):
        self._client = client
        self._device_id = device_id
        self._name = name
        self._position = 0

    @property
    def name(self):
        """Return the name of the cover."""
        return self._name

    @property
    def current_cover_position(self):
        """Return the current position of the cover."""
        return self._position

    async def async_set_cover_position(self, position):
        """Move the cover to a specific position."""
        await self._client.set_cover_position(self._device_id, position)
        self._position = position
        self.async_write_ha_state()

    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        await self.async_set_cover_position(100)

    async def async_close_cover(self, **kwargs):
        """Close the cover."""
        await self.async_set_cover_position(0)
