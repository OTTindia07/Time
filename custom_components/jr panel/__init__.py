"""The JR Touch Panel integration."""
import asyncio
import logging
from typing import Any, Dict

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, DEFAULT_PORT
from .panel import JRTouchPanel

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["switch", "fan", "light", "cover"]

async def async_setup(hass: HomeAssistant, config: Dict[str, Any]) -> bool:
    """Set up the JR Touch Panel component."""
    hass.data[DOMAIN] = {}
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up JR Touch Panel from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data.get(CONF_PORT, DEFAULT_PORT)
    name = entry.data.get(CONF_NAME, f"JR Touch Panel ({host})")

    panel = JRTouchPanel(hass, host, port, name)
    try:
        await panel.async_connect()
    except asyncio.TimeoutError:
        raise ConfigEntryNotReady(f"Timeout connecting to panel at {host}")

    hass.data[DOMAIN][entry.entry_id] = panel

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
