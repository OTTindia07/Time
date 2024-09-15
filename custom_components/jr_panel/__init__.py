"""Custom integration for JR Touch Panel"""
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
    host = entry.data["host"]
    port = entry.data.get("port", 4096)
    name = entry.data["name"]

    client = JRTouchPanelTCPClient(host, port)
    try:
        await client.connect()
    except Exception as e:
        _LOGGER.error(f"Failed to connect to JR Touch Panel at {host}:{port} - {str(e)}")
        return False

    switches = [
        JRTouchPanelSwitch(client, device_id, f"{name} Switch {i+1}")
        for i, device_id in enumerate(range(108, 118))
    ]

    fans = [
        JRTouchPanelFan(client, device_id, f"{name} Fan {i+1}")
        for i, device_id in enumerate(range(118, 120))
    ]

    dimmers = [
        JRTouchPanelDimmer(client, device_id, f"{name} Dimmer {i+1}")
        for i, device_id in enumerate(range(120, 124))
    ]

    covers = [
        JRTouchPanelCover(client, device_id, f"{name} Curtain {i+1}")
        for i, device_id in enumerate(range(124, 128, 2))
    ]

    entities = switches + fans + dimmers + covers
    hass.data[DOMAIN][entry.entry_id] = entities

    await hass.config_entries.async_forward_entry_setups(entry, ["switch", "light", "fan", "cover"])
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["switch", "light", "fan", "cover"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
  
