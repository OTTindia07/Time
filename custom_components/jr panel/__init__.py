import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .tcp_client import JRTouchPanelTCPClient
from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up JR Panel from configuration.yaml (if any)."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up JR Panel from a config entry."""
    host = entry.data["host"]
    port = entry.data["port"]

    _LOGGER.info(f"Setting up JR Panel for {host}:{port}")

    # Create the JR Panel client
    client = JRTouchPanelTCPClient(host, port)
    await client.connect()

    hass.data[DOMAIN][entry.entry_id] = client

    # Setup the platforms for the entry (switch, fan, light, cover)
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload JR Panel config entry."""
    _LOGGER.info(f"Unloading JR Panel for {entry.data['host']}")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .tcp_client import JRTouchPanelTCPClient
from .const import DOMAIN, PLATFORMS

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up JR Panel from configuration.yaml (if any)."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up JR Panel from a config entry."""
    host = entry.data["host"]
    port = entry.data["port"]

    _LOGGER.info(f"Setting up JR Panel for {host}:{port}")

    # Create the JR Panel client
    client = JRTouchPanelTCPClient(host, port)
    await client.connect()

    hass.data[DOMAIN][entry.entry_id] = client

    # Setup the platforms for the entry (switch, fan, light, cover)
    hass.config_entries.async_setup_platforms(entry, PLATFORMS)

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload JR Panel config entry."""
    _LOGGER.info(f"Unloading JR Panel for {entry.data['host']}")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok
