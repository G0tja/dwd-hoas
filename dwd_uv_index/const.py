"""Constants for the DWD UV Index integration."""

DOMAIN = "dwd_uv_index"

DWD_UVI_URL = "https://opendata.dwd.de/climate_environment/health/alerts/uvi.json"

CONF_CITY = "city"

# How often to poll (DWD updates once a day around 10:00 AM)
SCAN_INTERVAL_HOURS = 6

UV_RISK_LEVELS = {
    0: "None",
    1: "Low",
    2: "Low",
    3: "Moderate",
    4: "Moderate",
    5: "Moderate",
    6: "High",
    7: "High",
    8: "Very High",
    9: "Very High",
    10: "Very High",
    11: "Extreme",
}

UV_RISK_LEVEL_DE = {
    0: "Kein",
    1: "Gering",
    2: "Gering",
    3: "Mäßig",
    4: "Mäßig",
    5: "Mäßig",
    6: "Hoch",
    7: "Hoch",
    8: "Sehr hoch",
    9: "Sehr hoch",
    10: "Sehr hoch",
    11: "Extrem",
}
