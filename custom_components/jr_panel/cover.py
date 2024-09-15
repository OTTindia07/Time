from homeassistant.components.cover import CoverEntity

class JRTouchPanelCover(CoverEntity):
    """Representation of a JR Touch Panel cover (curtain)."""

    def __init__(self, client, device_id, name):
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
        """Set the cover position."""
        await self._client.set_cover_position(self._device_id, position)
        self._position = position
        self.async_write_ha_state()

    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        await self.async_set_cover_position(100)

    async def async_close_cover(self, **kwargs):
        """Close the cover."""
        await self.async_set_cover_position(0)

    async def async_stop_cover(self, **kwargs):
        """Stop the cover."""
        await self._client.stop_cover(self._device_id)
