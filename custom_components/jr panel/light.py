from homeassistant.components.light import LightEntity
from .tcp_client import JRTouchPanelTCPClient

class JRTouchPanelDimmer(LightEntity):
    """Representation of a dimmable light controlled by the JR Touch Panel."""

    def __init__(self, client: JRTouchPanelTCPClient, device_id: int, name: str):
        self.client = client
        self.device_id = device_id
        self._name = name
        self._brightness = 0

    @property
    def name(self):
        return self._name

    @property
    def brightness(self):
        return self._brightness

    async def async_turn_on(self, **kwargs):
        """Turn the dimmer on."""
        brightness = kwargs.get("brightness", 255)
        await self.client.send({"device_id": self.device_id, "brightness": brightness})
        self._brightness = brightness
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the dimmer off."""
        await self.client.send({"device_id": self.device_id, "brightness": 0})
        self._brightness = 0
        self.async_write_ha_state()
