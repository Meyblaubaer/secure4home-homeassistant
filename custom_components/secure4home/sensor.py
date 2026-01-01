"""Sensor platform for Secure4Home."""
import logging

from homeassistant.components.sensor import SensorEntity
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
    """Set up Secure4Home sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]

    entities = []

    # Add sensors for signal strength and connectivity
    if coordinator.data and "status" in coordinator.data:
        status_data = coordinator.data["status"].get("data", {})

        # RSSI (signal strength)
        if "rssi" in status_data:
            entities.append(
                Secure4HomeSensor(
                    coordinator,
                    "rssi",
                    "Secure4Home Signal Strength",
                    "signal_strength",
                )
            )

        # GSM RSSI
        if "gsm_rssi" in status_data:
            entities.append(
                Secure4HomeSensor(
                    coordinator,
                    "gsm_rssi",
                    "Secure4Home GSM Signal",
                    "signal_strength",
                )
            )

    async_add_entities(entities)


class Secure4HomeSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Secure4Home Sensor."""

    def __init__(
        self, coordinator, sensor_key: str, sensor_name: str, icon: str | None = None
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = sensor_name
        self._attr_unique_id = f"secure4home_{sensor_key}"
        self._sensor_key = sensor_key
        if icon:
            self._attr_icon = f"mdi:{icon}"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        if not self.coordinator.data or "status" not in self.coordinator.data:
            return None

        status_data = self.coordinator.data["status"].get("data", {})
        return status_data.get(self._sensor_key)
