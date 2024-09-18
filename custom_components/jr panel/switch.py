from homeassistant.components.switch import SwitchEntity
from .tcp_client import JRTouchPanelTCPClient

class JRTouchPanelSwitch(SwitchEntity):
    """Representation of a switch controlled by the JR Touch Panel."""

    def __init__(self, client: JRTouchPanelTCPClient, device_id: int, name: str):
        self.client = client
        self.device_id = device_id
        self._name = name
        self._state = False

    @property
    def name(self):
        return self._name

    @property
    def is_on(self):
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        await self.client.send({"device_id": self.device_id, "action": "on"})
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        await self.client.send({"device_id": self.device_id, "action": "off"})
        self._state = False
        self.async_write_ha_state()
