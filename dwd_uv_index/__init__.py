"""DWD UV Index integration for Home Assistant."""
from __future__ import annotations

import logging
from datetime import timedelta

import aiohttp
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DWD_UVI_URL, SCAN_INTERVAL_HOURS

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up DWD UV Index from a config entry."""
    session = async_get_clientsession(hass)

    coordinator = DWDUVIndexCoordinator(hass, session)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


class DWDUVIndexCoordinator(DataUpdateCoordinator):
    """Coordinator that fetches UV index data from DWD once every few hours."""

    def __init__(self, hass: HomeAssistant, session: aiohttp.ClientSession) -> None:
        """Initialise the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=SCAN_INTERVAL_HOURS),
        )
        self._session = session

    async def _async_update_data(self) -> dict:
        """Fetch data from DWD open-data endpoint."""
        try:
            async with async_timeout.timeout(30):
                resp = await self._session.get(DWD_UVI_URL)
                resp.raise_for_status()
                data = await resp.json(content_type=None)
        except aiohttp.ClientError as err:
            raise UpdateFailed(f"Error communicating with DWD: {err}") from err
        except Exception as err:  # noqa: BLE001
            raise UpdateFailed(f"Unexpected error fetching DWD data: {err}") from err

        # Build a dict keyed by city name for easy lookup
        cities: dict[str, dict] = {}
        for entry in data.get("content", []):
            city = entry.get("city", "")
            if city:
                cities[city] = entry.get("forecast", {})

        return {
            "last_update": data.get("last_update"),
            "next_update": data.get("next_update"),
            "forecast_day": data.get("forecast_day"),
            "cities": cities,
        }
