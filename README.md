# DWD Opendata Integration for Home Assistant

[![GitHub Release](https://img.shields.io/github/release/ian/dwd-hoas?style=flat-square)](https://github.com/ian/dwd-hoas/releases)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5?style=flat-square)](https://github.com/hacs/integration)

> ⚠️ **Personal Project - Limited Support**
> 
> This is a personal project created for my own use. It has **not been extensively tested** and **is not actively maintained**. Use at your own risk. Feel free to fork and maintain your own copy if needed.

This is a unified Home Assistant integration that provides both UV Index forecasts and pollen forecasts from the German meteorological service [Deutscher Wetterdienst (DWD)](https://www.dwd.de/).

## Features

- 🌞 Real-time UV Index forecasts for today, tomorrow, and the day after tomorrow
- 🌸 Pollen forecasts for 8 pollen types (grass, birch, alder, hazel, ash, mugwort, ambrosia, rye)
- 🌍 Support for 33+ pre-mapped German cities to pollen regions
- 📊 Easy configuration via the Home Assistant UI (Config Flow)
- 🔄 Automatic daily updates (UV: 6 hours, Pollen: 1 hour)
- 🇩🇪 German language support with translated status names
- 🎨 Dashboard-ready sensors with full attribute support

## Installation

### Via HACS (Home Assistant Community Store)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the "+" button
4. Search for "DWD Opendata"
5. Click "Install"
6. Restart Home Assistant

### Manual Installation

1. Clone this repository or download the latest release
2. Copy the `dwd_opendata` folder to `<config_dir>/custom_components/`
3. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "Create Integration" and search for "DWD Opendata"
3. Select your nearest DWD forecast station/city
4. Click "Create"

The integration will automatically:
- Fetch UV Index data from the DWD open data endpoint (every 6 hours)
- Fetch pollen data for the corresponding region (every hour)
- Create sensor entities for both data sources
- Update timestamps automatically

## Entities

The integration creates the following sensor entities:

### UV Index Sensors
- `sensor.<city>_uv_today` - UV Index for today
- `sensor.<city>_uv_tomorrow` - UV Index for tomorrow
- `sensor.<city>_uv_dayafter` - UV Index for the day after tomorrow

### Pollen Sensors (8 types)
- `sensor.pollen_graeser_<region_id>` - Grass pollen
- `sensor.pollen_birke_<region_id>` - Birch pollen
- `sensor.pollen_erle_<region_id>` - Alder pollen
- `sensor.pollen_hasel_<region_id>` - Hazel pollen
- `sensor.pollen_esche_<region_id>` - Ash pollen
- `sensor.pollen_beifuss_<region_id>` - Mugwort pollen
- `sensor.pollen_ambrosia_<region_id>` - Ambrosia pollen
- `sensor.pollen_roggen_<region_id>` - Rye pollen

## UV Index Risk Levels

The UV Index is classified into risk categories:

| Index | Risk Level (EN) | Risk Level (DE) |
|-------|-----------------|-----------------|
| 0-2   | Low             | Gering         |
| 3-5   | Moderate        | Mäßig          |
| 6-7   | High            | Hoch           |
| 8-10  | Very High       | Sehr hoch      |
| 11+   | Extreme         | Extrem         |

## Pollen Index Levels

Pollen forecasts use a 0-3 scale with 0.5 increments:

| Index | Description (German) |
|-------|----------------------|
| 0     | keine Belastung (no burden) |
| 0.5   | keine bis geringe (low) |
| 1     | geringe Belastung (low) |
| 1.5   | geringe bis mittlere (medium) |
| 2     | mittlere Belastung (medium) |
| 2.5   | mittlere bis hohe (high) |
| 3     | hohe Belastung (high) |

## Dashboard Examples

See [cards.md](cards.md) for complete examples of displaying UV Index and pollen forecasts using Mushroom Cards and other Lovelace components.

## Data Sources

All data is provided by the [Deutscher Wetterdienst (DWD)](https://www.dwd.de/) via their open data endpoints:
- UV Index: [opendata.dwd.de/climate_environment/health/alerts/uvi.json](https://opendata.dwd.de/climate_environment/health/alerts/uvi.json)
- Pollen: [opendata.dwd.de/climate_environment/health/alerts/s31fg.json](https://opendata.dwd.de/climate_environment/health/alerts/s31fg.json)

## Support

- 📖 [Home Assistant Documentation](https://www.home-assistant.io/)
- 🐛 [Issue Tracker](https://github.com/ian/dwd-hoas/issues)
- 💬 [Home Assistant Community Forums](https://community.home-assistant.io/)

## References

This integration combines functionality from two DWD integrations:
- **DWD UV Index** - Original UV Index integration
- **[DWD Pollenflug](https://github.com/mampfes/hacs_dwd_pollenflug)** - Pollen forecast integration by [@mampfes](https://github.com/mampfes)

The pollen data, examples, and region mapping are based on the excellent [DWD Pollenflug](https://github.com/mampfes/hacs_dwd_pollenflug) project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Data provided by [Deutscher Wetterdienst (DWD)](https://www.dwd.de/)
- Pollen integration based on [DWD Pollenflug](https://github.com/mampfes/hacs_dwd_pollenflug) by [@mampfes](https://github.com/mampfes)
- Built for the amazing [Home Assistant](https://www.home-assistant.io/) community

