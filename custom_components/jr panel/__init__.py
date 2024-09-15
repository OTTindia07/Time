import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .tcp_client import JRTouchPanelTCPClient

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the JR Touch Panel integration."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up JR Touch Panel from a config entry."""
    host = entry.data.get("host")
    port = entry.data.get("port", 4096)
    name = entry.data.get("name")

    _LOGGER.info(f"Setting up JR Touch Panel for {name} ({host}:{port})")

    client = JRTouchPanelTCPClient(host, port)
    await client.connect()

    # Storing the client for later use
    hass.data[DOMAIN][entry.entry_id] = client

    # Setup the platforms for the entry (switch, fan, light, cover)
    hass.config_entries.async_setup_platforms(entry, ["switch", "fan", "light", "cover"])
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info(f"Unloading JR Touch Panel for {entry.data['name']}")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["switch", "fan", "light", "cover"])

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
