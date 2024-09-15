"""Config flow for JR Touch Panel integration."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PORT
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_PORT, DOMAIN
from .jr_accessory import JRAccessory

_LOGGER = logging.getLogger(__name__)

class JRPanelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JR Touch Panel."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                accessory = JRAccessory(self.hass, user_input)
                await accessory.connect()
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_HOST): str,
                    vol.Required(CONF_NAME): str,
                    vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
                }
            ),
            errors=errors,
        )

    async def async_step_zeroconf(self, discovery_info):
        """Handle zeroconf discovery."""
        _LOGGER.debug("Discovered JR Touch Panel via zeroconf: %s", discovery_info)

        host = discovery_info.host
        name = discovery_info.name
        port = discovery_info.port or DEFAULT_PORT
        unique_id = discovery_info.hostname

        await self.async_set_unique_id(unique_id)
        self._abort_if_unique_id_configured()

        self.context["title_placeholders"] = {"name": name}

        return await self.async_step_user(
            user_input={CONF_HOST: host, CONF_NAME: name, CONF_PORT: port}
        )
