"""Config flow for DWD UV Index."""
from __future__ import annotations

import logging
from typing import Any

import aiohttp
import async_timeout
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_CITY, DOMAIN, DWD_UVI_URL

_LOGGER = logging.getLogger(__name__)


async def _fetch_cities(hass: HomeAssistant) -> list[str]:
    """Download the DWD JSON and return the sorted list of available cities."""
    session = async_get_clientsession(hass)
    async with async_timeout.timeout(30):
        resp = await session.get(DWD_UVI_URL)
        resp.raise_for_status()
        data = await resp.json(content_type=None)
    return sorted(
        entry["city"]
        for entry in data.get("content", [])
        if entry.get("city")
    )


class DWDUVIndexConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for DWD UV Index."""

    VERSION = 1

    def __init__(self) -> None:
        self._cities: list[str] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step: let the user pick their city."""
        errors: dict[str, str] = {}

        if not self._cities:
            try:
                self._cities = await _fetch_cities(self.hass)
            except aiohttp.ClientError:
                errors["base"] = "cannot_connect"
            except Exception:  # noqa: BLE001
                _LOGGER.exception("Unexpected error fetching DWD city list")
                errors["base"] = "unknown"

        if user_input is not None and not errors:
            city = user_input[CONF_CITY]

            # Prevent duplicate entries for the same city
            await self.async_set_unique_id(f"dwd_uv_{city}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"DWD UV Index – {city}",
                data={CONF_CITY: city},
            )

        city_options = self._cities or []

        schema = vol.Schema(
            {
                vol.Required(CONF_CITY, default=city_options[0] if city_options else ""): vol.In(city_options)
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "url": DWD_UVI_URL,
            },
        )
