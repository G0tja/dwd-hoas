"""Constants for the DWD Opendata integration."""

DOMAIN = "dwd_opendata"

# UV Index API
DWD_UVI_URL = "https://opendata.dwd.de/climate_environment/health/alerts/uvi.json"
CONF_CITY = "city"

# Pollenflug API
DWD_POLLENFLUG_URL = "https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json"
CONF_REGION_ID = "region_id"

# How often to poll (DWD updates once a day around 10:00 AM)
SCAN_INTERVAL_HOURS = 6
SCAN_INTERVAL_HOURS_POLLEN = 1

# UV Risk levels for display
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

# City to Pollenflug region mapping
CITY_TO_REGION_ID = {
    "Arkona": 20,
    "Berlin": 50,
    "Bremen": 31,
    "Cottbus": 50,
    "Dresden": 81,
    "Düsseldorf": 41,
    "Frankfurt/Main": 92,
    "Freiburg": 111,
    "Großer Arber": 82,
    "Hahn": 62,
    "Hamburg": 12,
    "Hannover": 32,
    "Kahler Asten": 62,
    "Kassel": 91,
    "Konstanz": 111,
    "Leipzig": 81,
    "List auf Sylt": 11,
    "Magdeburg": 61,
    "Marienleuchte": 122,
    "München": 121,
    "Neubrandenburg": 20,
    "Norderney": 11,
    "Nürnberg": 123,
    "Osnabrück": 42,
    "Regensburg": 122,
    "Rostock": 20,
    "Seehausen": 31,
    "Stuttgart": 112,
    "Waren": 20,
    "Weimar": 71,
    "Weinbiet": 101,
    "Wernigerode": 62,
    "Würzburg": 123,
}
