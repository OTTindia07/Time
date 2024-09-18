from homeassistant.components.fan import FanEntity
from .tcp_client import JRTouchPanelTCPClient

class JRTouchPanelFan(FanEntity):
    """Representation of a fan controlled by the JR Touch Panel."""

    def __init__(self, client: JRTouchPanelTCPClient, device_id: int, name: str):
        self.client = client
        self.device_id = device_id
        self._name = name
        self._speed = 0

    @property
    def name(self):
        return self._name

    @property
    def percentage(self):
        return self._speed

    async def async_set_percentage(self, percentage: int):
        """Set the speed of the fan."""
        await self.client.send({"device_id": self.device_id, "speed": percentage})
        self._speed = percentage
        self.async_write_ha_state()
