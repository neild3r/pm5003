"""Support for PMS5003 Particulate Matter Sensor."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import (
    CONF_PIN_ENABLE,
    CONF_PIN_RESET,
    CONF_SERIAL_DEVICE,
    DEFAULT_NAME,
    DEFAULT_PIN_ENABLE,
    DEFAULT_PIN_RESET,
    DEFAULT_SCAN_INTERVAL,
    DEFAULT_SERIAL_DEVICE,
    DOMAIN,
    PMS5003SensorEntityDescription,
    SENSOR_TYPES,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up PMS5003 sensor based on a config entry."""
    config = hass.data[DOMAIN][entry.entry_id]

    serial_device = config.get(CONF_SERIAL_DEVICE, DEFAULT_SERIAL_DEVICE)
    pin_enable = config.get(CONF_PIN_ENABLE, DEFAULT_PIN_ENABLE)
    pin_reset = config.get(CONF_PIN_RESET, DEFAULT_PIN_RESET)

    coordinator = PMS5003DataUpdateCoordinator(
        hass,
        serial_device=serial_device,
        pin_enable=pin_enable,
        pin_reset=pin_reset,
    )

    await coordinator.async_config_entry_first_refresh()

    entities = [
        PMS5003Sensor(coordinator, description, entry) for description in SENSOR_TYPES
    ]

    async_add_entities(entities)


class PMS5003DataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching PMS5003 data."""

    def __init__(
        self,
        hass: HomeAssistant,
        serial_device: str,
        pin_enable: str,
        pin_reset: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self._serial_device = serial_device
        self._pin_enable = pin_enable
        self._pin_reset = pin_reset
        self._pms5003 = None

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from PMS5003 sensor."""
        try:
            return await self.hass.async_add_executor_job(self._read_sensor)
        except Exception as err:
            raise UpdateFailed(f"Error reading PMS5003 sensor: {err}") from err

    def _read_sensor(self) -> dict[str, Any]:
        """Read data from the PMS5003 sensor (runs in executor)."""
        from pms5003 import PMS5003, ReadTimeoutError, SerialTimeoutError

        if self._pms5003 is None:
            self._pms5003 = PMS5003(
                device=self._serial_device,
                baudrate=9600,
                pin_enable=self._pin_enable,
                pin_reset=self._pin_reset,
            )

        try:
            data = self._pms5003.read()

            return {
                # PM concentration (standard factory environment)
                "pm1_0": data.pm_ug_per_m3(1.0, atmospheric_environment=False),
                "pm2_5": data.pm_ug_per_m3(2.5, atmospheric_environment=False),
                "pm10": data.pm_ug_per_m3(10, atmospheric_environment=False),
                # PM concentration (atmospheric environment)
                "pm1_0_atm": data.pm_ug_per_m3(1.0, atmospheric_environment=True),
                "pm2_5_atm": data.pm_ug_per_m3(2.5, atmospheric_environment=True),
                "pm10_atm": data.pm_ug_per_m3(None, atmospheric_environment=True),
                # Particle counts per 0.1L air
                "particles_0_3": data.pm_per_1l_air(0.3),
                "particles_0_5": data.pm_per_1l_air(0.5),
                "particles_1_0": data.pm_per_1l_air(1.0),
                "particles_2_5": data.pm_per_1l_air(2.5),
                "particles_5_0": data.pm_per_1l_air(5),
                "particles_10": data.pm_per_1l_air(10),
            }
        except (ReadTimeoutError, SerialTimeoutError) as err:
            _LOGGER.warning("PMS5003 read timeout: %s", err)
            raise


class PMS5003Sensor(CoordinatorEntity, SensorEntity):
    """Representation of a PMS5003 sensor."""

    entity_description: PMS5003SensorEntityDescription

    def __init__(
        self,
        coordinator: PMS5003DataUpdateCoordinator,
        description: PMS5003SensorEntityDescription,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name=DEFAULT_NAME,
            manufacturer="Plantower",
            model="PMS5003",
        )

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get(self.entity_description.key)
