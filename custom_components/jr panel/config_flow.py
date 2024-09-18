import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import aiohttp_client
from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_NAME, DEFAULT_PORT

class JRPanelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JR Touch Panel."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            # Test connection to JR Touch Panel using the provided info
            try:
                client = JRTouchPanelTCPClient(user_input[CONF_HOST], user_input.get(CONF_PORT, DEFAULT_PORT))
                await client.connect()
                await client.disconnect()

                # Create the entry
                return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
            except Exception:
                errors["base"] = "cannot_connect"

        # Show the form if input is None or there were errors
        data_schema = vol.Schema({
            vol.Required(CONF_NAME): str,
            vol.Required(CONF_HOST): str,
            vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
        })
        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return JRPanelOptionsFlowHandler(config_entry)


class JRPanelOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for JR Touch Panel."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options_schema = vol.Schema({})
        return self.async_show_form(step_id="init", data_schema=options_schema)
