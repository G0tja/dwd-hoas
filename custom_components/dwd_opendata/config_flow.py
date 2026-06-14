"""Config flow for DWD Opendata integration."""
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

from .const import CITY_TO_REGION_ID, CONF_CITY, CONF_REGION_ID, DOMAIN, DWD_UVI_URL

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


class DWDOpendataConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for DWD Opendata."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
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

            # Get region ID for this city
            region_id = CITY_TO_REGION_ID.get(city)
            if region_id is None:
                _LOGGER.warning("City %s not in mapping, using fallback region", city)
                region_id = 50  # Fallback to Brandenburg und Berlin

            # Prevent duplicate entries for the same city
            await self.async_set_unique_id(f"dwd_opendata_{city}")
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"DWD Opendata – {city}",
                data={CONF_CITY: city, CONF_REGION_ID: region_id},
            )

        city_options = self._cities or []

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_CITY, default=city_options[0] if city_options else ""
                ): vol.In(city_options)
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
            description_placeholders={
                "uvi_url": DWD_UVI_URL,
            },
        )
