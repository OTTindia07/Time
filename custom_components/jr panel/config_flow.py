import logging
from typing import Dict, Optional

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_HOST, CONF_PORT, CONF_NAME

_LOGGER = logging.getLogger(__name__)

class JRPanelConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JR Touch Panel integration."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize the config flow."""
        self._host = None
        self._port = None
        self._name = None

    async def async_step_user(self, user_input: Optional[Dict[str, str]] = None) -> FlowResult:
        """Handle the initial step of user input."""
        if user_input is not None:
            self._host = user_input[CONF_HOST]
            self._port = user_input[CONF_PORT]
            self._name = user_input[CONF_NAME]

            # Validate the input
            if not self._validate_connection(self._host, self._port):
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._get_data_schema(),
                    errors={"base": "cannot_connect"},
                )

            # Check if already configured
            if self._is_already_configured(self._host, self._port):
                return self.async_abort(reason="already_configured")

            # Save the configuration
            return self.async_create_entry(
                title=self._name,
                data={
                    CONF_HOST: self._host,
                    CONF_PORT: self._port,
                    CONF_NAME: self._name,
                },
            )

        # Show the configuration form
        return self.async_show_form(
            step_id="user",
            data_schema=self._get_data_schema(),
        )

    def _get_data_schema(self):
        """Return the data schema for the user input form."""
        from homeassistant.helpers import config_validation as cv
        import voluptuous as vol

        return vol.Schema(
            {
                vol.Required(CONF_HOST, default=""): cv.string,
                vol.Required(CONF_PORT, default=4096): cv.port,
                vol.Required(CONF_NAME, default="JR Touch Panel"): cv.string,
            }
        )

    def _validate_connection(self, host: str, port: int) -> bool:
        """Validate connection to the JR Touch Panel."""
        from aiohttp import ClientSession

        async def validate(host: str, port: int) -> bool:
            """Check if we can connect to the host and port."""
            try:
                async with ClientSession() as session:
                    async with session.get(f"http://{host}:{port}") as response:
                        return response.status == 200
            except Exception as e:
                _LOGGER.error(f"Error connecting to {host}:{port} - {e}")
                return False

        return asyncio.run(validate(host, port))

    def _is_already_configured(self, host: str, port: int) -> bool:
        """Check if the configuration is already set up."""
        existing_entries = self._async_current_entries()
        for entry in existing_entries:
            if entry.data.get(CONF_HOST) == host and entry.data.get(CONF_PORT) == port:
                return True
        return False
