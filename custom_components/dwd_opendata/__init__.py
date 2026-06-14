"""DWD Opendata integration for UV Index and Pollen forecasts."""
from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

import aiohttp
import async_timeout
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import CONF_CITY, CONF_REGION_ID, DOMAIN, DWD_POLLENFLUG_URL, DWD_UVI_URL, SCAN_INTERVAL_HOURS, SCAN_INTERVAL_HOURS_POLLEN
from .DWD.Pollenflug import Pollenflug

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up DWD Opendata from a config entry."""
    hass.data.setdefault(DOMAIN, {})

    city = entry.data[CONF_CITY]
    region_id = entry.data[CONF_REGION_ID]

    # Initialize coordinator for UV Index
    coordinator = OpendataCoordinator(hass, city)

    # Initialize shell for Pollenflug
    shell = hass.data[DOMAIN].get("shell")
    if shell is None:
        shell = OpendataShell(hass)
        hass.data[DOMAIN]["shell"] = shell

    # Fetch initial data
    try:
        await coordinator.async_config_entry_first_refresh()
    except ConfigEntryNotReady:
        raise

    try:
        await hass.async_add_executor_job(shell._fetch)
    except Exception as exc:
        _LOGGER.error("Fetch pollen data from DWD failed: %s", exc)
        raise ConfigEntryNotReady from exc

    # Store coordinator for this entry
    hass.data[DOMAIN][entry.entry_id] = {
        "coordinator": coordinator,
        "shell": shell,
        "city": city,
        "region_id": region_id,
    }

    # Register entry with shell
    shell.add_entry(entry, region_id)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        if entry.entry_id in hass.data[DOMAIN]:
            shell = hass.data[DOMAIN][entry.entry_id].get("shell")
            del hass.data[DOMAIN][entry.entry_id]

            if shell:
                shell.remove_entry(entry)
                if shell.is_idle():
                    del hass.data[DOMAIN]["shell"]

        if not hass.data[DOMAIN]:
            del hass.data[DOMAIN]

    return unload_ok


class OpendataCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator for UV Index data from DWD."""

    def __init__(self, hass: HomeAssistant, city: str) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=SCAN_INTERVAL_HOURS),
        )
        self._city = city
        self._session = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch UV Index data from DWD."""
        try:
            async with async_timeout.timeout(30):
                resp = await self._session.get(DWD_UVI_URL)
                resp.raise_for_status()
                data = await resp.json(content_type=None)
        except asyncio.TimeoutError as err:
            raise UpdateFailed("Timeout fetching UV Index data") from err
        except aiohttp.ClientError as err:
            raise UpdateFailed("Error fetching UV Index data") from err

        # Parse UV Index data
        cities_data = {}
        last_update = None
        next_update = None
        forecast_day = None

        for entry in data.get("content", []):
            city_name = entry.get("city")
            if city_name:
                cities_data[city_name] = entry.get("forecast", {})

        if data.get("content"):
            last_update = data.get("last_update")
            next_update = data.get("next_update")
            forecast_day = data.get("forecast_day")

        return {
            "cities": cities_data,
            "last_update": last_update,
            "next_update": next_update,
            "forecast_day": forecast_day,
        }


class OpendataShell:
    """Shell object for DWD Pollenflug data. Stored in hass.data."""

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the instance."""
        self._hass = hass
        self._source = Pollenflug()
        self._entries: dict[str, int] = {}  # entry_id -> region_id
        self._fetch_callback_listener = None

    @property
    def source(self) -> Pollenflug:
        """Return the Pollenflug data source."""
        return self._source

    def add_entry(self, config_entry: ConfigEntry, region_id: int) -> None:
        """Add entry."""
        if self.is_idle():
            # This is the first entry, therefore start the timer
            self._fetch_callback_listener = async_track_time_interval(
                self._hass, self._fetch_callback, timedelta(hours=SCAN_INTERVAL_HOURS_POLLEN)
            )

        self._entries[config_entry.entry_id] = region_id

    def remove_entry(self, config_entry: ConfigEntry) -> None:
        """Remove entry."""
        self._entries.pop(config_entry.entry_id, None)

        if self.is_idle() and self._fetch_callback_listener is not None:
            # This was the last region, therefore stop the timer
            self._fetch_callback_listener()
            self._fetch_callback_listener = None

    def is_idle(self) -> bool:
        """Check if no entries are active."""
        return not bool(self._entries)

    @callback
    def _fetch_callback(self, *_: Any) -> None:
        """Schedule pollen data fetch."""
        self._hass.add_job(self._fetch)

    def _fetch(self, *_: Any) -> None:
        """Fetch pollen data from DWD."""
        try:
            self._source.fetch()
        except Exception as error:
            _LOGGER.error("Fetch pollen data from DWD failed: %s", error)
