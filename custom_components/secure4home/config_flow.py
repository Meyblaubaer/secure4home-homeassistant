"""Config flow for Secure4Home integration."""
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.data_entry_flow import FlowResult

from .api import Secure4HomeAPI
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class Secure4HomeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Secure4Home."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                # Test the credentials
                api = Secure4HomeAPI(
                    user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
                )
                await api.login()
                await api.close()

                # Create the entry
                return self.async_create_entry(
                    title=user_input[CONF_USERNAME], data=user_input
                )

            except Exception:
                _LOGGER.exception("Unexpected exception during login")
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_USERNAME): str,
                    vol.Required(CONF_PASSWORD): str,
                }
            ),
            errors=errors,
        )
