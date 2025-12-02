# PMS5003 Home Assistant Integration

[![HACS Default](https://img.shields.io/badge/HACS-Default-blue.svg)](https://github.com/hacs/integration)

A Home Assistant custom integration for the PMS5003 Particulate Matter Sensor using the [Pimoroni pms5003-python](https://github.com/pimoroni/pms5003-python) library.

## Features

This integration provides sensors for:

### PM Concentration (Standard Factory Environment)
- **PM1.0**: Ultrafine particles (µg/m³)
- **PM2.5**: Combustion particles, organic compounds, metals (µg/m³)
- **PM10**: Dust, pollen, mould spores (µg/m³)

### PM Concentration (Atmospheric Environment)
- **PM1.0 Atmospheric**: PM1.0 under atmospheric conditions (µg/m³)
- **PM2.5 Atmospheric**: PM2.5 under atmospheric conditions (µg/m³)
- **PM10 Atmospheric**: PM10 under atmospheric conditions (µg/m³)

### Particle Counts (per 0.1L of air)
- **Particles >0.3µm**
- **Particles >0.5µm**
- **Particles >1.0µm**
- **Particles >2.5µm**
- **Particles >5.0µm**
- **Particles >10µm**

## Requirements

- Raspberry Pi (or compatible device) with GPIO support
- PMS5003 Particulate Matter Sensor connected via serial
- Python 3.9+
- Home Assistant 2023.1.0+

## Hardware Setup

1. Connect the PMS5003 sensor to your Raspberry Pi:
   - VCC to 5V
   - GND to GND
   - TX to RX (GPIO15 / Pin 10)
   - RX to TX (GPIO14 / Pin 8)
   - Enable to GPIO22 (configurable)
   - Reset to GPIO27 (configurable)

2. Enable serial on your Raspberry Pi:
   - Run `sudo raspi-config`
   - Navigate to Interface Options > Serial Port
   - Disable serial login shell
   - Enable serial port hardware

3. Add `dtoverlay=pi3-miniuart-bt` to `/boot/config.txt`

4. Reboot your Raspberry Pi

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add `https://github.com/neild3r/pm5003` as a custom repository with category "Integration"
6. Click "Add"
7. Search for "PMS5003" and install it
8. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/pms5003` directory from this repository
2. Copy it to your Home Assistant `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** > **Devices & Services**
2. Click **+ Add Integration**
3. Search for "PMS5003"
4. Configure the settings:
   - **Serial Device**: Path to the serial device (default: `/dev/ttyAMA0`)
   - **Enable GPIO Pin**: GPIO pin for enabling the sensor (default: `GPIO22`)
   - **Reset GPIO Pin**: GPIO pin for resetting the sensor (default: `GPIO27`)

## Dashboard Example

Add cards to your Home Assistant dashboard to display air quality data:

```yaml
type: entities
title: Air Quality
entities:
  - entity: sensor.pms5003_pm2_5
    name: PM2.5
  - entity: sensor.pms5003_pm10
    name: PM10
  - entity: sensor.pms5003_pm1_0
    name: PM1.0
```

Or use a gauge card for PM2.5:

```yaml
type: gauge
entity: sensor.pms5003_pm2_5
name: PM2.5
min: 0
max: 500
severity:
  green: 0
  yellow: 35
  red: 55
```

## Troubleshooting

### Serial Device Not Found

- Ensure the serial device path is correct (usually `/dev/ttyAMA0` or `/dev/serial0`)
- Check that serial is enabled in `raspi-config`
- Verify the `dtoverlay=pi3-miniuart-bt` line is in `/boot/config.txt`

### Read Timeout Errors

- Check the physical connections to the sensor
- Ensure the enable and reset GPIO pins are correctly connected
- The sensor may need a few seconds to warm up after power-on

### Permission Denied

- Add your user to the `dialout` group: `sudo usermod -a -G dialout $USER`
- Or run Home Assistant with appropriate permissions

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

- [Pimoroni pms5003-python](https://github.com/pimoroni/pms5003-python) - The underlying Python library for the PMS5003 sensor
- [Home Assistant](https://www.home-assistant.io/) - The amazing home automation platform
