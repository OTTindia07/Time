"""Cover service for JR Touch Panel."""
from homeassistant.components.cover import CoverEntity

from .abstract_service import AbstractService

class JRCover(CoverEntity, AbstractService):
    """Representation of a JR Touch Panel cover."""

    @property
    def is_closed(self):
        """Return true if the cover is closed."""
        return self.accessory.entities[self.dp_id]["value"] == 0

    async def async_close_cover(self, **kwargs):
        """Close the cover."""
        await self.set_state(0)

    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        await self.set_state(100)

    async def update(self):
        """Update the cover state."""
        self.accessory.entities[self.dp_id]["value"] = await self.accessory.get_state(self.dp_id)
