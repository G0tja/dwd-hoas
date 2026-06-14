# DWD UV Index Integration for Home Assistant

[![GitHub Release](https://img.shields.io/github/release/ian/dwd-hoas?style=flat-square)](https://github.com/ian/dwd-hoas/releases)
[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![HACS](https://img.shields.io/badge/HACS-Default-41BDF5?style=flat-square)](https://github.com/hacs/integration)

> ⚠️ **Personal Project - Limited Support**
> 
> This is a personal project created for my own use. It has **not been extensively tested** and **is not actively maintained**. Use at your own risk. Feel free to fork and maintain your own copy if needed.

This is a Home Assistant integration that provides UV Index forecasts from the German meteorological service [Deutscher Wetterdienst (DWD)](https://www.dwd.de/).

## Features

- 🌞 Real-time UV Index forecasts for today, tomorrow, and the day after tomorrow
- 🌍 Support for 40+ German cities and regions
- 📊 Easy configuration via the Home Assistant UI (Config Flow)
- 🔄 Automatic daily updates (configurable interval)
- 🇩🇪 German language support with translated status names

## Installation

### Via HACS (Home Assistant Community Store)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the "+" button
4. Search for "DWD UV Index"
5. Click "Install"
6. Restart Home Assistant

### Manual Installation

1. Clone this repository or download the latest release
2. Copy the `dwd_uv_index` folder to `<config_dir>/custom_components/`
3. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "Create Automation" and select "DWD UV Index"
3. Select your nearest DWD forecast station/city
4. Click "Create"

The integration will automatically:
- Fetch data from the DWD open data endpoint
- Update every 6 hours (configurable in the manifest)
- Create sensor entities for UV Index forecasts

## Entities

The integration creates the following sensor entities:

- `sensor.dwd_uv_index_<city>_uv_today` - UV Index for today
- `sensor.dwd_uv_index_<city>_uv_tomorrow` - UV Index for tomorrow
- `sensor.dwd_uv_index_<city>_uv_dayafter` - UV Index for the day after tomorrow

## UV Index Risk Levels

The UV Index is classified into risk categories:

| Index | Risk Level (EN) | Risk Level (DE) |
|-------|-----------------|-----------------|
| 0-2   | Low             | Gering         |
| 3-5   | Moderate        | Mäßig          |
| 6-7   | High            | Hoch           |
| 8-10  | Very High       | Sehr hoch      |
| 11+   | Extreme         | Extrem         |

## Data Source

All data is provided by the [Deutscher Wetterdienst](https://www.dwd.de/) via their [open data endpoint](https://opendata.dwd.de/climate_environment/health/alerts/). The service provides daily UV Index forecasts updated around 10:00 AM CET.

## Support

- 📖 [Home Assistant Documentation](https://www.home-assistant.io/)
- 🐛 [Issue Tracker](https://github.com/ian/dwd-hoas/issues)
- 💬 [Home Assistant Community Forums](https://community.home-assistant.io/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Data provided by [Deutscher Wetterdienst (DWD)](https://www.dwd.de/)
- Built for the amazing [Home Assistant](https://www.home-assistant.io/) community
