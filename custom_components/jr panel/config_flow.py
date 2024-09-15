import logging
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class JRConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JR Panel."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            try:
                # Validate connection to JR Panel
                host = user_input["host"]
                port = user_input["port"]
                name = user_input["name"]
                # Create entry
                return self.async_create_entry(title=name, data=user_input)
            except Exception as e:
                _LOGGER.error(f"Failed to connect: {e}")
                errors["base"] = "cannot_connect"

        data_schema = {
            "host": str,
            "port": int,
            "name": str,
        }

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Options flow handler."""
        return JRPanelOptionsFlow(config_entry)

class JRPanelOptionsFlow(config_entries.OptionsFlow):
    """Handle the options flow."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Handle the initial step."""
        return self.async_show_form(step_id="init", data_schema={})
