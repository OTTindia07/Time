from homeassistant.components.fan import FanEntity, SUPPORT_SET_SPEED

class JRTouchPanelFan(FanEntity):
    """Representation of a JR Touch Panel fan."""

    def __init__(self, client, device_id, name):
        self._client = client
        self._device_id = device_id
        self._name = name
        self._speed = 0

    @property
    def name(self):
        """Return the name of the fan."""
        return self._name

    @property
    def speed(self):
        """Return the current speed of the fan."""
        return self._speed

    @property
    def speed_list(self):
        """Return the list of available speeds."""
        return [0, 25, 50, 75, 100]

    @property
    def supported_features(self):
        """Flag supported features."""
        return SUPPORT_SET_SPEED

    async def async_set_speed(self, speed):
        """Set the fan speed."""
        if speed in self.speed_list:
            await self._client.set_fan_speed(self._device_id, speed)
            self._speed = speed
            self.async_write_ha_state()

    async def async_turn_on(self, speed=None, **kwargs):
        """Turn the fan on."""
        await self.async_set_speed(speed if speed else 25)

    async def async_turn_off(self, **kwargs):
        """Turn the fan off."""
        await self.async_set_speed(0)
        
