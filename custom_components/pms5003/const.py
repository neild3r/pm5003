"""Constants for the PMS5003 Particulate Matter Sensor integration."""

from __future__ import annotations

from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
)

DOMAIN = "pms5003"
DEFAULT_NAME = "PMS5003"

# Configuration keys
CONF_SERIAL_DEVICE = "serial_device"
CONF_PIN_ENABLE = "pin_enable"
CONF_PIN_RESET = "pin_reset"

# Defaults
DEFAULT_SERIAL_DEVICE = "/dev/ttyAMA0"
DEFAULT_PIN_ENABLE = "GPIO22"
DEFAULT_PIN_RESET = "GPIO27"
DEFAULT_SCAN_INTERVAL = 30  # seconds

# Unit for particle count
UNIT_PARTICLES_PER_DL = "particles/0.1L"


@dataclass(frozen=True)
class PMS5003SensorEntityDescription(SensorEntityDescription):
    """Describes PMS5003 sensor entity."""

    size: float | None = None
    atmospheric: bool = False
    particle_count: bool = False


SENSOR_TYPES: tuple[PMS5003SensorEntityDescription, ...] = (
    # PM concentration (standard factory environment)
    PMS5003SensorEntityDescription(
        key="pm1_0",
        name="PM1.0",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.PM1,
        state_class=SensorStateClass.MEASUREMENT,
        size=1.0,
        atmospheric=False,
    ),
    PMS5003SensorEntityDescription(
        key="pm2_5",
        name="PM2.5",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.PM25,
        state_class=SensorStateClass.MEASUREMENT,
        size=2.5,
        atmospheric=False,
    ),
    PMS5003SensorEntityDescription(
        key="pm10",
        name="PM10",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.PM10,
        state_class=SensorStateClass.MEASUREMENT,
        size=10,
        atmospheric=False,
    ),
    # PM concentration (atmospheric environment)
    PMS5003SensorEntityDescription(
        key="pm1_0_atm",
        name="PM1.0 Atmospheric",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.PM1,
        state_class=SensorStateClass.MEASUREMENT,
        size=1.0,
        atmospheric=True,
    ),
    PMS5003SensorEntityDescription(
        key="pm2_5_atm",
        name="PM2.5 Atmospheric",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.PM25,
        state_class=SensorStateClass.MEASUREMENT,
        size=2.5,
        atmospheric=True,
    ),
    PMS5003SensorEntityDescription(
        key="pm10_atm",
        name="PM10 Atmospheric",
        native_unit_of_measurement=CONCENTRATION_MICROGRAMS_PER_CUBIC_METER,
        device_class=SensorDeviceClass.PM10,
        state_class=SensorStateClass.MEASUREMENT,
        size=None,  # API uses None for atmospheric PM10
        atmospheric=True,
    ),
    # Particle counts per 0.1L air
    PMS5003SensorEntityDescription(
        key="particles_0_3",
        name="Particles >0.3µm",
        native_unit_of_measurement=UNIT_PARTICLES_PER_DL,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:blur",
        size=0.3,
        particle_count=True,
    ),
    PMS5003SensorEntityDescription(
        key="particles_0_5",
        name="Particles >0.5µm",
        native_unit_of_measurement=UNIT_PARTICLES_PER_DL,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:blur",
        size=0.5,
        particle_count=True,
    ),
    PMS5003SensorEntityDescription(
        key="particles_1_0",
        name="Particles >1.0µm",
        native_unit_of_measurement=UNIT_PARTICLES_PER_DL,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:blur",
        size=1.0,
        particle_count=True,
    ),
    PMS5003SensorEntityDescription(
        key="particles_2_5",
        name="Particles >2.5µm",
        native_unit_of_measurement=UNIT_PARTICLES_PER_DL,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:blur",
        size=2.5,
        particle_count=True,
    ),
    PMS5003SensorEntityDescription(
        key="particles_5_0",
        name="Particles >5.0µm",
        native_unit_of_measurement=UNIT_PARTICLES_PER_DL,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:blur",
        size=5,
        particle_count=True,
    ),
    PMS5003SensorEntityDescription(
        key="particles_10",
        name="Particles >10µm",
        native_unit_of_measurement=UNIT_PARTICLES_PER_DL,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:blur",
        size=10,
        particle_count=True,
    ),
)
