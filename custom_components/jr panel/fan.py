from homeassistant.components.fan import FanEntity
from .tcp_client import JRTouchPanelTCPClient

class JRTouchPanelFan(FanEntity):
    """Representation of a JR Touch Panel fan."""

    def __init__(self, client: JRTouchPanelTCPClient, device_id: int, name: str):
        self._client = client
        self._device_id = device_id
        self._name = name
        self._speed = 0

    @property
    def name(self):
        """Return the name of the fan."""
        return self._name

    @property
    def percentage(self):
        """Return the current speed of the fan as a percentage."""
        return self._speed

    async def async_set_percentage(self, percentage):
        """Set the fan speed."""
        await self._client.set_fan_speed(self._device_id, percentage)
        self._speed = percentage
        self.async_write_ha_state()

    async def async_turn_on(self, speed=None, **kwargs):
        """Turn on the fan."""
        if speed is None:
            speed = 25
        await self.async_set_percentage(speed)

    async def async_turn_off(self, **kwargs):
        """Turn off the fan."""
        await self.async_set_percentage(0)
