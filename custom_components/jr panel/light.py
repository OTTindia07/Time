"""Light service for JR Touch Panel."""
from homeassistant.components.light import LightEntity

from .abstract_service import AbstractService

class JRLight(LightEntity, AbstractService):
    """Representation of a JR Touch Panel light."""

    @property
    def is_on(self):
        """Return true if the light is on."""
        return self.accessory.entities[self.dp_id]["value"]

    async def async_turn_on(self, **kwargs):
        """Turn the light on."""
        await self.set_state(True)

    async def async_turn_off(self, **kwargs):
        """Turn the light off."""
        await self.set_state(False)

    async def update(self):
        """Update the light state."""
        self.accessory.entities[self.dp_id]["value"] = await self.accessory.get_state(self.dp_id)
