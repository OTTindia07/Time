import logging
from typing import Any, Dict

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class JRConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for JR Touch Panel."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    async def async_step_user(self, user_input: Dict[str, Any] = None) -> FlowResult:
        """Handle the initial step of configuration."""
        if user_input is not None:
            # Validate user input and create the entry
            host = user_input.get("host")
            name = user_input.get("name")
            port = user_input.get("port", 4096)

            # Basic validation
            if not host:
                return self.async_show_form(
                    step_id="user",
                    data_schema=self._get_data_schema(),
                    errors={"base": "host_required"}
                )

            # Check if entry already exists
            existing_entries = self._async_current_entries()
            if any(entry.data["host"] == host for entry in existing_entries):
                return self.async_abort(reason="already_configured")

            # Proceed to create an entry
            return self.async_create_entry(
                title=name,
                data={"host": host, "name": name, "port": port}
            )

        # Show form to the user for configuration
        return self.async_show_form(
            step_id="user",
            data_schema=self._get_data_schema()
        )

    def _get_data_schema(self):
        """Return the schema for user input."""
        from homeassistant.helpers import config_entry_flow

        return config_entry_flow.DataSchema(
            {
                "host": str,
                "name": str,
                "port": int,
            }
        )

    async def async_step_zeroconf(self, discovery_info: Dict[str, Any]) -> FlowResult:
        """Handle zeroconf discovery."""
        # Extract details from discovery_info and set up the configuration
        host = discovery_info.get("host")
        name = discovery_info.get("name")
        port = discovery_info.get("port", 4096)

        if host:
            return self.async_create_entry(
                title=name,
                data={"host": host, "name": name, "port": port}
            )

        return self.async_abort(reason="cannot_connect")
