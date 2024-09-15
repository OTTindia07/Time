from homeassistant.components.switch import SwitchEntity
from .tcp_client import JRTouchPanelTCPClient

class JRTouchPanelSwitch(SwitchEntity):
    """Representation of a JR Touch Panel switch."""

    def __init__(self, client: JRTouchPanelTCPClient, device_id: int, name: str):
        self._client = client
        self._device_id = device_id
        self._name = name
        self._state = False

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        await self._client.set_switch_state(self._device_id, True)
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        await self._client.set_switch_state(self._device_id, False)
        self._state = False
        self.async_write_ha_state()
