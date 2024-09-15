import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class JRPanelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JR Touch Panel."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input["host"]
            name = user_input["name"]
            port = user_input.get("port", 4096)

            # Add logic to test the connection here
            try:
                return self.async_create_entry(title=name, data={"host": host, "port": port, "name": name})
            except Exception as e:
                _LOGGER.error("Failed to connect to JR Touch Panel: %s", e)
                errors["base"] = "cannot_connect"

        data_schema = vol.Schema(
            {
                vol.Required("host"): str,
                vol.Optional("name", default="JR Panel"): str,
                vol.Optional("port", default=4096): int,
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return JRPanelOptionsFlow(config_entry)

class JRPanelOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for JR Touch Panel."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        return self.async_show_form(step_id="init")
