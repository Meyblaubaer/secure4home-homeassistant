"""Binary sensor platform for Secure4Home."""
import logging

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Secure4Home binary sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = []

    # Add binary sensors for system status (tamper, etc.)
    if coordinator.data and "status" in coordinator.data:
        status_data = coordinator.data["status"].get("data", {})

        # Tamper sensor
        if "tamper" in status_data:
            entities.append(
                Secure4HomeStatusBinarySensor(
                    coordinator,
                    "tamper",
                    "Secure4Home Tamper",
                    BinarySensorDeviceClass.TAMPER,
                )
            )

        # AC Fail sensor (power)
        if "acfail" in status_data:
            entities.append(
                Secure4HomeStatusBinarySensor(
                    coordinator,
                    "acfail",
                    "Secure4Home AC Power",
                    BinarySensorDeviceClass.POWER,
                )
            )

        # Battery sensor
        if "battery" in status_data:
            entities.append(
                Secure4HomeStatusBinarySensor(
                    coordinator,
                    "battery",
                    "Secure4Home Battery",
                    BinarySensorDeviceClass.BATTERY,
                )
            )

    async_add_entities(entities)


class Secure4HomeStatusBinarySensor(CoordinatorEntity, BinarySensorEntity):
    """Representation of a Secure4Home Status Binary Sensor."""

    def __init__(
        self,
        coordinator,
        sensor_key: str,
        sensor_name: str,
        device_class: BinarySensorDeviceClass | None = None,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._attr_name = sensor_name
        self._attr_unique_id = f"secure4home_{sensor_key}"
        self._attr_device_class = device_class
        self._sensor_key = sensor_key

    @property
    def is_on(self) -> bool | None:
        """Return true if the binary sensor is on."""
        if not self.coordinator.data or "status" not in self.coordinator.data:
            return None

        status_data = self.coordinator.data["status"].get("data", {})
        value = status_data.get(self._sensor_key, "")

        # Parse status value (e.g., "main.normal" or "main.abnormal")
        if isinstance(value, str):
            # For tamper, jam: "abnormal" means triggered (ON)
            if self._sensor_key in ["tamper", "jam"]:
                return "abnormal" in value.lower()
            # For acfail, battery: "normal" means OK (ON for power/battery good)
            elif self._sensor_key in ["acfail", "battery"]:
                return "normal" in value.lower()

        return None
