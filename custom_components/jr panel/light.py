from homeassistant.components.light import LightEntity
from .tcp_client import JRTouchPanelTCPClient

class JRTouchPanelDimmer(LightEntity):
    """Representation of a JR Touch Panel dimmer."""

    def __init__(self, client: JRTouchPanelTCPClient, device_id: int, name: str):
        self._client = client
        self._device_id = device_id
        self._name = name
        self._brightness = 0

    @property
    def name(self):
        """Return the name of the dimmer."""
        return self._name

    @property
    def brightness(self):
        """Return the brightness of the dimmer."""
        return self._brightness

    async def async_turn_on(self, **kwargs):
        """Turn on the dimmer."""
        brightness = kwargs.get('brightness', 255)
        await self._client.set_dimmer_brightness(self._device_id, brightness)
        self._brightness = brightness
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off the dimmer."""
        await self._client.set_dimmer_brightness(self._device_id, 0)
        self._brightness = 0
        self.async_write_ha_state()
