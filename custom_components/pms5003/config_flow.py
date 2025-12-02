"""Config flow for PMS5003 Particulate Matter Sensor integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError

from .const import (
    CONF_PIN_ENABLE,
    CONF_PIN_RESET,
    CONF_SERIAL_DEVICE,
    DEFAULT_NAME,
    DEFAULT_PIN_ENABLE,
    DEFAULT_PIN_RESET,
    DEFAULT_SERIAL_DEVICE,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_SERIAL_DEVICE, default=DEFAULT_SERIAL_DEVICE): str,
        vol.Required(CONF_PIN_ENABLE, default=DEFAULT_PIN_ENABLE): str,
        vol.Required(CONF_PIN_RESET, default=DEFAULT_PIN_RESET): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    # Validate that the serial device exists
    serial_device = data[CONF_SERIAL_DEVICE]

    def check_device():
        import os

        if not os.path.exists(serial_device):
            raise CannotConnect(f"Serial device {serial_device} does not exist")

    try:
        await hass.async_add_executor_job(check_device)
    except FileNotFoundError as err:
        raise CannotConnect(f"Serial device {serial_device} not found") from err

    return {"title": DEFAULT_NAME}


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for PMS5003."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                # Check if already configured
                await self.async_set_unique_id(user_input[CONF_SERIAL_DEVICE])
                self._abort_if_unique_id_configured()

                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""
