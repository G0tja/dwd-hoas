"""Sensor platform for DWD Opendata integration."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
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
from homeassistant.util.dt import utcnow

from . import OpendataCoordinator, OpendataShell
from .const import CONF_CITY, CONF_REGION_ID, DOMAIN, UV_RISK_LEVELS


@dataclass(frozen=True)
class DWDUVSensorEntityDescription(SensorEntityDescription):
    """Describe a DWD UV Index sensor."""

    forecast_key: str = "today"


UV_SENSOR_DESCRIPTIONS: tuple[DWDUVSensorEntityDescription, ...] = (
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

ATTR_VAL_TOMORROW = "state_tomorrow"
ATTR_VAL_IN_2_DAYS = "state_in_2_days"
ATTR_DESC_TODAY = "state_today_desc"
ATTR_DESC_TOMORROW = "state_tomorrow_desc"
ATTR_DESC_IN_2_DAYS = "state_in_2_days_desc"
ATTR_LAST_UPDATE = "last_update"
ATTR_NEXT_UPDATE = "next_update"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up DWD Opendata sensors from a config entry."""
    data = hass.data[DOMAIN][entry.entry_id]
    coordinator: OpendataCoordinator = data["coordinator"]
    shell: OpendataShell = data["shell"]
    city: str = entry.data[CONF_CITY]
    region_id: int = entry.data[CONF_REGION_ID]

    entities = []

    # Add UV Index sensors
    for description in UV_SENSOR_DESCRIPTIONS:
        entities.append(
            DWDUVSensor(
                coordinator,
                description,
                city,
                entry.entry_id,
            )
        )

    # Add Pollen sensors
    source = shell.source
    names = set()
    for pollen in source.pollen_list:
        if pollen.region_id == region_id and pollen.name not in names:
            names.add(pollen.name)
            entities.append(
                DWDPollenSensor(
                    hass,
                    source,
                    region_id,
                    pollen.name,
                    entry.entry_id,
                )
            )

    async_add_entities(entities)


class DWDUVSensor(CoordinatorEntity[OpendataCoordinator], SensorEntity):
    """Sensor representing the DWD UV index for a specific day."""

    entity_description: DWDUVSensorEntityDescription

    def __init__(
        self,
        coordinator: OpendataCoordinator,
        description: DWDUVSensorEntityDescription,
        city: str,
        entry_id: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._city = city
        self._attr_unique_id = f"{DOMAIN}_{entry_id}_{description.key}"
        self._attr_name = f"{city} {description.name}"
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": f"DWD Opendata – {city}",
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


class DWDPollenSensor(SensorEntity):
    """Sensor representing DWD pollen forecast for a specific type and region."""

    def __init__(
        self,
        hass: HomeAssistant,
        source: Any,
        region_id: int,
        pollen_name: str,
        entry_id: str,
    ) -> None:
        """Initialize the sensor."""
        self._hass = hass
        self._source = source
        self._region_id = region_id
        self._pollen_name = pollen_name
        self._value = None

        self._attr_unique_id = f"{DOMAIN}_{entry_id}_pollen_{pollen_name}"
        self._attr_name = f"Pollen {pollen_name} {region_id}"
        self._attr_icon = "mdi:flower-pollen"
        region_name = "Unknown"
        if region_id in self._source.regions_list:
            region_name = self._source.regions_list[region_id].name

        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry_id)},
            "name": f"DWD Opendata – Region {region_id}",
            "manufacturer": self._source.sender,
            "model": region_name,
            "entry_type": "service",
        }
        self._attr_state_class = SensorStateClass.MEASUREMENT

    async def async_update(self) -> None:
        """Update the value of the entity."""
        today = utcnow().date()

        val_today = None
        val_tomorrow = None
        val_in_2_days = None

        for pollen in self._source.pollen_list:
            if pollen.region_id == self._region_id and pollen.name == self._pollen_name:
                if pollen.date == today:
                    val_today = pollen.value
                elif pollen.date == today + timedelta(days=1):
                    val_tomorrow = pollen.value
                elif pollen.date == today + timedelta(days=2):
                    val_in_2_days = pollen.value

        self._value = val_today
        attributes = {
            ATTR_VAL_TOMORROW: val_tomorrow,
            ATTR_VAL_IN_2_DAYS: val_in_2_days,
            ATTR_DESC_TODAY: self._source.legend.get(val_today),
            ATTR_DESC_TOMORROW: self._source.legend.get(val_tomorrow),
            ATTR_DESC_IN_2_DAYS: self._source.legend.get(val_in_2_days),
            ATTR_LAST_UPDATE: self._source.last_update,
            ATTR_NEXT_UPDATE: self._source.next_update,
        }
        self._attr_extra_state_attributes = attributes
        self._attr_attribution = f"Last update: {self._source.last_update.astimezone()}"

    @property
    def available(self) -> bool:
        """Return true if value is valid."""
        return self._value is not None

    @property
    def native_value(self) -> float | None:
        """Return the value of the entity."""
        return self._value


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
