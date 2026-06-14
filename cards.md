# Displaying DWD UV Index with Mushroom Card

This guide shows how to display the DWD UV Index data using the [Mushroom Card](https://github.com/piitaya/lovelace-mushroom) template.

## Prerequisites

1. Install the [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) custom component from HACS
2. Have the DWD UV Index integration installed and configured

## Basic Temperature Card (Today's UV Index)

```yaml
type: custom:mushroom-template-card
entity: sensor.dwd_uv_index_<city>_uv_today
primary: UV Index Today
secondary: "{{ state_attr(entity, 'friendly_name') }}"
icon: mdi:sun-wireless
icon_color: |
  {% set uv = state_attr(entity, 'unit_of_measurement') %}
  {% if state_attr(entity, 'value', 0) | int(0) <= 2 %}
    green
  {% elif state_attr(entity, 'value', 0) | int(0) <= 5 %}
    yellow
  {% elif state_attr(entity, 'value', 0) | int(0) <= 7 %}
    orange
  {% elif state_attr(entity, 'value', 0) | int(0) <= 10 %}
    red
  {% else %}
    purple
  {% endif %}
```

## Advanced UV Index Card with Status

```yaml
type: custom:mushroom-template-card
entity: sensor.dwd_uv_index_<city>_uv_today
primary: UV Index
secondary: |
  {% set uv = states(entity) | int(0) %}
  {% if uv <= 2 %}
    {{ uv }} - Low Risk
  {% elif uv <= 5 %}
    {{ uv }} - Moderate Risk
  {% elif uv <= 7 %}
    {{ uv }} - High Risk
  {% elif uv <= 10 %}
    {{ uv }} - Very High Risk
  {% else %}
    {{ uv }} - Extreme Risk
  {% endif %}
icon: mdi:sun-wireless
icon_color: |
  {% set uv = states(entity) | int(0) %}
  {% if uv <= 2 %}
    green
  {% elif uv <= 5 %}
    yellow
  {% elif uv <= 7 %}
    orange
  {% elif uv <= 10 %}
    red
  {% else %}
    purple
  {% endif %}
```

## Three-Day Forecast Grid

```yaml
type: grid
columns: 3
cards:
  - type: custom:mushroom-template-card
    entity: sensor.dwd_uv_index_<city>_uv_today
    primary: Today
    secondary: |
      {% set uv = states(entity) | int(0) %}
      {% if uv <= 2 %}
        {{ uv }} - Low Risk
      {% elif uv <= 5 %}
        {{ uv }} - Moderate Risk
      {% elif uv <= 7 %}
        {{ uv }} - High Risk
      {% elif uv <= 10 %}
        {{ uv }} - Very High Risk
      {% else %}
        {{ uv }} - Extreme Risk
      {% endif %}
    icon: mdi:calendar-today
    icon_color: |
      {% set uv = states(entity) | int(0) %}
      {% if uv <= 2 %}
        green
      {% elif uv <= 5 %}
        yellow
      {% elif uv <= 7 %}
        orange
      {% elif uv <= 10 %}
        red
      {% else %}
        purple
      {% endif %}

  - type: custom:mushroom-template-card
    entity: sensor.dwd_uv_index_<city>_uv_tomorrow
    primary: Tomorrow
    secondary: |
      {% set uv = states(entity) | int(0) %}
      {% if uv <= 2 %}
        {{ uv }} - Low Risk
      {% elif uv <= 5 %}
        {{ uv }} - Moderate Risk
      {% elif uv <= 7 %}
        {{ uv }} - High Risk
      {% elif uv <= 10 %}
        {{ uv }} - Very High Risk
      {% else %}
        {{ uv }} - Extreme Risk
      {% endif %}
    icon: mdi:calendar-plus-1
    icon_color: |
      {% set uv = states(entity) | int(0) %}
      {% if uv <= 2 %}
        green
      {% elif uv <= 5 %}
        yellow
      {% elif uv <= 7 %}
        orange
      {% elif uv <= 10 %}
        red
      {% else %}
        purple
      {% endif %}

  - type: custom:mushroom-template-card
    entity: sensor.dwd_uv_index_<city>_uv_dayafter
    primary: Day After
    secondary: |
      {% set uv = states(entity) | int(0) %}
      {% if uv <= 2 %}
        {{ uv }} - Low Risk
      {% elif uv <= 5 %}
        {{ uv }} - Moderate Risk
      {% elif uv <= 7 %}
        {{ uv }} - High Risk
      {% elif uv <= 10 %}
        {{ uv }} - Very High Risk
      {% else %}
        {{ uv }} - Extreme Risk
      {% endif %}
    icon: mdi:calendar-plus-2
    icon_color: |
      {% set uv = states(entity) | int(0) %}
      {% if uv <= 2 %}
        green
      {% elif uv <= 5 %}
        yellow
      {% elif uv <= 7 %}
        orange
      {% elif uv <= 10 %}
        red
      {% else %}
        purple
      {% endif %}
```

## Compact Info Card with Multiple Days

```yaml
type: custom:mushroom-template-card
primary: UV Index Forecast
secondary: |
  Today: {{ states('sensor.dwd_uv_index_<city>_uv_today') }}
  Tomorrow: {{ states('sensor.dwd_uv_index_<city>_uv_tomorrow') }}
  Day After: {{ states('sensor.dwd_uv_index_<city>_uv_dayafter') }}
icon: mdi:sun-wireless
multiline_secondary: true
```

## UV Index Color Scale Reference

| UV Index | Risk Level   | Color  |
|----------|--------------|--------|
| 0-2      | Low          | 🟢 green    |
| 3-5      | Moderate     | 🟡 yellow   |
| 6-7      | High         | 🟠 orange   |
| 8-10     | Very High    | 🔴 red      |
| 11+      | Extreme      | 🟣 purple   |

## Customization Tips

- **Replace `<city>`** with your actual city name (e.g., `Berlin`, `Munich`)
- **Icons**: Other sun-related icons available: `mdi:sun`, `mdi:sun-outline`, `mdi:weather-sunny`
- **Colors**: Use any Home Assistant color name or hex code (e.g., `#FF5722`)
- **Layout**: Combine with other cards in a grid or vertical stack for a dashboard

## Example Complete Dashboard Section

```yaml
type: vertical-stack
cards:
  - type: heading
    heading: UV Index Forecast

  - type: grid
    columns: 3
    cards:
      - type: custom:mushroom-template-card
        entity: sensor.dwd_uv_index_<city>_uv_today
        primary: Today
        secondary: |
          {% set uv = states(entity) | int(0) %}
          {% if uv <= 2 %}
            {{ uv }} - Low Risk
          {% elif uv <= 5 %}
            {{ uv }} - Moderate Risk
          {% elif uv <= 7 %}
            {{ uv }} - High Risk
          {% elif uv <= 10 %}
            {{ uv }} - Very High Risk
          {% else %}
            {{ uv }} - Extreme Risk
          {% endif %}
        icon: mdi:calendar-today
        icon_color: orange

      - type: custom:mushroom-template-card
        entity: sensor.dwd_uv_index_<city>_uv_tomorrow
        primary: Tomorrow
        secondary: |
          {% set uv = states(entity) | int(0) %}
          {% if uv <= 2 %}
            {{ uv }} - Low Risk
          {% elif uv <= 5 %}
            {{ uv }} - Moderate Risk
          {% elif uv <= 7 %}
            {{ uv }} - High Risk
          {% elif uv <= 10 %}
            {{ uv }} - Very High Risk
          {% else %}
            {{ uv }} - Extreme Risk
          {% endif %}
        icon: mdi:calendar-plus-1
        icon_color: orange

      - type: custom:mushroom-template-card
        entity: sensor.dwd_uv_index_<city>_uv_dayafter
        primary: Day After
        secondary: |
          {% set uv = states(entity) | int(0) %}
          {% if uv <= 2 %}
            {{ uv }} - Low Risk
          {% elif uv <= 5 %}
            {{ uv }} - Moderate Risk
          {% elif uv <= 7 %}
            {{ uv }} - High Risk
          {% elif uv <= 10 %}
            {{ uv }} - Very High Risk
          {% else %}
            {{ uv }} - Extreme Risk
          {% endif %}
        icon: mdi:calendar-plus-2
        icon_color: orange
```

## Troubleshooting

- **Entity not found**: Make sure your sensor entity exists. Check in Developer Tools → States
- **Icons not showing**: Verify you're using valid Material Design Icons (MDI) names
- **Colors not updating**: Check the template syntax in your YAML

---

# Displaying Pollen Forecasts with Mushroom Cards

This section shows how to display the DWD Pollen forecast data using the [Mushroom Card](https://github.com/piitaya/lovelace-mushroom) template. Based on examples from the [DWD Pollenflug](https://github.com/mampfes/hacs_dwd_pollenflug) project.

## Prerequisites

1. Install the [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) custom component from HACS
2. Have the DWD Opendata integration installed and configured
3. Replace `<region_id>` with your configured region ID (shown in entity names like `sensor.pollen_graeser_124`)

## Pollen Index Scale

| Index | Description (German) | Status  | Color |
|-------|----------------------|---------|-------|
| 0     | keine Belastung      | None    | 🟢 green |
| 0.5   | keine bis geringe    | Low     | 🟢 green |
| 1     | geringe Belastung    | Low     | 🟢 green |
| 1.5   | geringe bis mittlere  | Medium  | 🟡 orange |
| 2     | mittlere Belastung   | Medium  | 🟡 orange |
| 2.5   | mittlere bis hohe    | High    | 🔴 red |
| 3     | hohe Belastung       | High    | 🔴 red |

## Minimal Pollen Grid (All 8 Pollen Types)

```yaml
square: true
type: grid
columns: 4
cards:
  - type: custom:mushroom-template-card
    entity: sensor.pollen_graeser_<region_id>
    primary: Gras
    icon: mdi:grass
    layout: vertical
    icon_color: |-
      {% if states(config.entity) | float <= 1 %}
        green
      {% elif states(config.entity) | float <= 2 %}
        orange
      {% else %}
        red
      {% endif %}
    tap_action:
      action: more-info

  - type: custom:mushroom-template-card
    entity: sensor.pollen_ambrosia_<region_id>
    primary: Ambrosia
    icon: mdi:flower-pollen
    layout: vertical
    icon_color: |-
      {% if states(config.entity) | float <= 1 %}
        green
      {% elif states(config.entity) | float <= 2 %}
        orange
      {% else %}
        red
      {% endif %}
    tap_action:
      action: more-info

  - type: custom:mushroom-template-card
    entity: sensor.pollen_birke_<region_id>
    primary: Birke
    icon: mdi:flower-pollen
    layout: vertical
    icon_color: |-
      {% if states(config.entity) | float <= 1 %}
        green
      {% elif states(config.entity) | float <= 2 %}
        orange
      {% else %}
        red
      {% endif %}
    tap_action:
      action: more-info

  - type: custom:mushroom-template-card
    entity: sensor.pollen_erle_<region_id>
    primary: Erle
    icon: mdi:flower-pollen
    layout: vertical
    icon_color: |-
      {% if states(config.entity) | float <= 1 %}
        green
      {% elif states(config.entity) | float <= 2 %}
        orange
      {% else %}
        red
      {% endif %}
    tap_action:
      action: more-info

  - type: custom:mushroom-template-card
    entity: sensor.pollen_hasel_<region_id>
    primary: Hasel
    icon: mdi:flower-pollen
    layout: vertical
    icon_color: |-
      {% if states(config.entity) | float <= 1 %}
        green
      {% elif states(config.entity) | float <= 2 %}
        orange
      {% else %}
        red
      {% endif %}
    tap_action:
      action: more-info

  - type: custom:mushroom-template-card
    entity: sensor.pollen_esche_<region_id>
    primary: Esche
    icon: mdi:flower-pollen
    layout: vertical
    icon_color: |-
      {% if states(config.entity) | float <= 1 %}
        green
      {% elif states(config.entity) | float <= 2 %}
        orange
      {% else %}
        red
      {% endif %}
    tap_action:
      action: more-info

  - type: custom:mushroom-template-card
    entity: sensor.pollen_beifuss_<region_id>
    primary: Beifuss
    icon: mdi:flower-pollen
    layout: vertical
    icon_color: |-
      {% if states(config.entity) | float <= 1 %}
        green
      {% elif states(config.entity) | float <= 2 %}
        orange
      {% else %}
        red
      {% endif %}
    tap_action:
      action: more-info

  - type: custom:mushroom-template-card
    entity: sensor.pollen_roggen_<region_id>
    primary: Roggen
    icon: mdi:flower-pollen
    layout: vertical
    icon_color: |-
      {% if states(config.entity) | float <= 1 %}
        green
      {% elif states(config.entity) | float <= 2 %}
        orange
      {% else %}
        red
      {% endif %}
    tap_action:
      action: more-info
```

## Pollen Forecast with Description

Shows today's and tomorrow's forecast with German descriptions:

```yaml
square: true
type: grid
columns: 2
cards:
  - type: custom:mushroom-template-card
    entity: sensor.pollen_graeser_<region_id>
    primary: Gras
    secondary: |-
      Today: {{ state_attr('sensor.pollen_graeser_<region_id>', 'state_today_desc') }}
      Tomorrow: {{ state_attr('sensor.pollen_graeser_<region_id>', 'state_tomorrow_desc') }}
    icon: mdi:grass
    layout: vertical
    icon_color: |-
      {% if states(config.entity) | float <= 1 %}
        green
      {% elif states(config.entity) | float <= 2 %}
        orange
      {% else %}
        red
      {% endif %}
    multiline_secondary: true
    tap_action:
      action: more-info

  - type: custom:mushroom-template-card
    entity: sensor.pollen_erle_<region_id>
    primary: Erle
    secondary: |-
      Today: {{ state_attr('sensor.pollen_erle_<region_id>', 'state_today_desc') }}
      Tomorrow: {{ state_attr('sensor.pollen_erle_<region_id>', 'state_tomorrow_desc') }}
    icon: mdi:flower-pollen
    layout: vertical
    icon_color: |-
      {% if states(config.entity) | float <= 1 %}
        green
      {% elif states(config.entity) | float <= 2 %}
        orange
      {% else %}
        red
      {% endif %}
    multiline_secondary: true
    tap_action:
      action: more-info
```

## Combined UV Index and Pollen Dashboard

```yaml
type: vertical-stack
cards:
  - type: heading
    heading: Weather Forecasts
    heading_tag: h2

  - type: heading
    heading: UV Index
    heading_tag: h3

  - type: grid
    columns: 3
    cards:
      - type: custom:mushroom-template-card
        entity: sensor.berlin_uv_today
        primary: Today
        icon: mdi:sun-wireless
        icon_color: orange

      - type: custom:mushroom-template-card
        entity: sensor.berlin_uv_tomorrow
        primary: Tomorrow
        icon: mdi:sun-wireless-outline
        icon_color: orange

      - type: custom:mushroom-template-card
        entity: sensor.berlin_uv_dayafter
        primary: Day After
        icon: mdi:sun-wireless-outline
        icon_color: orange

  - type: heading
    heading: Pollen Forecast
    heading_tag: h3

  - type: grid
    columns: 4
    square: true
    cards:
      - type: custom:mushroom-template-card
        entity: sensor.pollen_graeser_<region_id>
        primary: Gras
        icon: mdi:grass
        layout: vertical
        icon_color: |-
          {% if states(config.entity) | float <= 1 %}
            green
          {% elif states(config.entity) | float <= 2 %}
            orange
          {% else %}
            red
          {% endif %}

      - type: custom:mushroom-template-card
        entity: sensor.pollen_erle_<region_id>
        primary: Erle
        icon: mdi:flower-pollen
        layout: vertical
        icon_color: |-
          {% if states(config.entity) | float <= 1 %}
            green
          {% elif states(config.entity) | float <= 2 %}
            orange
          {% else %}
            red
          {% endif %}

      - type: custom:mushroom-template-card
        entity: sensor.pollen_birke_<region_id>
        primary: Birke
        icon: mdi:flower-pollen
        layout: vertical
        icon_color: |-
          {% if states(config.entity) | float <= 1 %}
            green
          {% elif states(config.entity) | float <= 2 %}
            orange
          {% else %}
            red
          {% endif %}

      - type: custom:mushroom-template-card
        entity: sensor.pollen_hasel_<region_id>
        primary: Hasel
        icon: mdi:flower-pollen
        layout: vertical
        icon_color: |-
          {% if states(config.entity) | float <= 1 %}
            green
          {% elif states(config.entity) | float <= 2 %}
            orange
          {% else %}
            red
          {% endif %}
```

## Customization Tips

- **Entity IDs**: Find your pollen region ID in Home Assistant Developer Tools → States (e.g., `sensor.pollen_graeser_124` has region_id `124`)
- **Colors**: Pollen uses 3-tier system (green ≤1, orange ≤2, red >2) vs UV's 5-tier system
- **Attributes**: Each pollen sensor includes `state_today_desc`, `state_tomorrow_desc`, `state_in_2_days_desc` for German descriptions
- **Icons**: Use `mdi:grass` for grass, `mdi:flower-pollen` for other pollen types, or other pollen-related MDI icons

---

## References

- [Original DWD Pollenflug Integration](https://github.com/mampfes/hacs_dwd_pollenflug) - The pollen forecast component that inspired this unified integration
- [DWD Pollen Information](https://www.dwd.de/DE/leistungen/gefahrenindizespollen/gefahrenindexpollen.html) - Official German Meteorological Service (DWD) pollen information
- [Mushroom Cards](https://github.com/piitaya/lovelace-mushroom) - Custom Lovelace card component used in these examples
