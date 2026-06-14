"""Sensor platform for DWD UV Index."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import DWDUVIndexCoordinator
from .const import CONF_CITY, DOMAIN, UV_RISK_LEVELS


@dataclass(frozen=True)
class DWDUVSensorEntityDescription(SensorEntityDescription):
    """Describe a DWD UV Index sensor."""
    forecast_key: str = "today"


SENSOR_DESCRIPTIONS: tuple[DWDUVSensorEntityDescription, ...] = (
    DWDUVSensorEntityDescription(
        key="uv_today",
        name="UV Index Today",
        icon="mdi:sun-wireless",
        state_class=SensorStateClass.MEASUREMENT,
        forecast_key="today",
    ),
    DWDUVSensorEntityDescription(
        key="uv_tomorrow",
        name="UV Index Tomorrow",
        icon="mdi:sun-wireless-outline",
        state_class=None,
        forecast_key="tomorrow",
    ),
    DWDUVSensorEntityDescription(
        key="uv_dayafter",
        name="UV Index Day After Tomorrow",
        icon="mdi:sun-wireless-outline",
        state_class=None,
        forecast_key="dayafter_to",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up DWD UV Index sensors from a config entry."""
    coordinator: DWDUVIndexCoordinator = hass.data[DOMAIN][entry.entry_id]
    city: str = entry.data[CONF_CITY]

    async_add_entities(
        DWDUVIndexSensor(coordinator, description, city, entry.entry_id)
        for description in SENSOR_DESCRIPTIONS
    )


class DWDUVIndexSensor(CoordinatorEntity[DWDUVIndexCoordinator], SensorEntity):
    """Sensor representing the DWD UV index for a specific day."""

    entity_description: DWDUVSensorEntityDescription

    def __init__(
        self,
        coordinator: DWDUVIndexCoordinator,
        description: DWDUVSensorEntityDescription,
        city: str,
        entry_id: str,
    ) -> None:
        """Initialise the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._city = city
        self._attr_unique_id = f"{entry_id}_{description.key}"
        self._attr_name = f"{city} {description.name}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": f"DWD UV Index – {city}",
            "manufacturer": "Deutscher Wetterdienst",
            "model": "UV Hazard Index",
            "configuration_url": "https://www.dwd.de/uvi",
        }

    @property
    def native_value(self) -> int | None:
        """Return the UV index value."""
        forecast = self.coordinator.data.get("cities", {}).get(self._city)
        if forecast is None:
            return None
        value = forecast.get(self.entity_description.forecast_key)
        return int(value) if value is not None else None

    @property
    def native_unit_of_measurement(self) -> str:
        """UV index is dimensionless."""
        return "UV index"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes."""
        value = self.native_value
        attrs: dict[str, Any] = {
            "city": self._city,
            "last_update": self.coordinator.data.get("last_update"),
            "next_update": self.coordinator.data.get("next_update"),
            "forecast_day": self.coordinator.data.get("forecast_day"),
            "data_source": "DWD opendata (opendata.dwd.de)",
        }
        if value is not None:
            attrs["risk_level"] = UV_RISK_LEVELS.get(min(value, 11), "Extreme")
            attrs["protection_advice"] = _protection_advice(value)
        return attrs


def _protection_advice(uvi: int) -> str:
    """Return a short sun-protection recommendation based on the UV index."""
    if uvi <= 2:
        return "No protection required."
    if uvi <= 5:
        return "Protection recommended: sunscreen SPF 30+, hat and sunglasses."
    if uvi <= 7:
        return "Protection essential: SPF 50+, seek shade during midday hours."
    if uvi <= 10:
        return "Extra protection needed: SPF 50+, avoid sun 10 AM–4 PM."
    return "Maximum protection: stay indoors during peak hours if possible."
