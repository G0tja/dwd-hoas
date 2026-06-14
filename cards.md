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
