from homeassistant.components.light import LightEntity, ATTR_BRIGHTNESS

class JRTouchPanelDimmer(LightEntity):
    """Representation of a JR Touch Panel dimmer."""

    def __init__(self, client, device_id, name):
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

    @property
    def is_on(self):
        """Return true if dimmer is on."""
        return self._brightness > 0

    async def async_turn_on(self, **kwargs):
        """Turn on the dimmer."""
        brightness = kwargs.get(ATTR_BRIGHTNESS, 255)  # Default to full brightness
        scaled_brightness = int(brightness / 255 * 100)  # Scale to 0-100 for JR panel
        await self._client.set_dimmer_brightness(self._device_id, scaled_brightness)
        self._brightness = brightness
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off the dimmer."""
        await self._client.set_dimmer_brightness(self._device_id, 0)
        self._brightness = 0
        self.async_write_ha_state()
        
