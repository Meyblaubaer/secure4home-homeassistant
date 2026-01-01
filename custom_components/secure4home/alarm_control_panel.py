"""Alarm control panel for Secure4Home."""
import logging

from homeassistant.components.alarm_control_panel import (
    AlarmControlPanelEntity,
    AlarmControlPanelEntityFeature,
    AlarmControlPanelState,
    CodeFormat,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, MODE_ARM, MODE_DISARM, MODE_HOME

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Secure4Home alarm control panel."""
    coordinator = hass.data[DOMAIN][entry.entry_id]["coordinator"]
    api = hass.data[DOMAIN][entry.entry_id]["api"]

    # Create alarm panel entities for each area
    entities = []
    if coordinator.data and "mode" in coordinator.data:
        # Get areas from mode data (response.data is an array)
        mode_response = coordinator.data["mode"]
        areas = mode_response.get("data", [])

        for area_data in areas:
            area_id = area_data.get("area", "1")
            area_name = area_data.get("area_name", "")
            entities.append(
                Secure4HomeAlarmPanel(coordinator, api, area_id, area_name)
            )

    # Fallback: if no areas found, create one default area
    if not entities:
        entities.append(Secure4HomeAlarmPanel(coordinator, api, "1", "Area 1"))

    async_add_entities(entities)


class Secure4HomeAlarmPanel(CoordinatorEntity, AlarmControlPanelEntity):
    """Representation of a Secure4Home Alarm Panel."""

    _attr_supported_features = (
        AlarmControlPanelEntityFeature.ARM_HOME
        | AlarmControlPanelEntityFeature.ARM_AWAY
    )

    def __init__(self, coordinator, api, area_id: str, area_name: str | None) -> None:
        """Initialize the alarm panel."""
        super().__init__(coordinator)
        self._api = api
        self._area_id = area_id
        self._attr_name = area_name or f"Secure4Home Area {area_id}"
        self._attr_unique_id = f"secure4home_area_{area_id}"
        self._attr_code_arm_required = True
        self._attr_code_format = CodeFormat.NUMBER
        self._attr_supported_features = (
            AlarmControlPanelEntityFeature.ARM_HOME
            | AlarmControlPanelEntityFeature.ARM_AWAY
        )

    @property
    def code_format(self) -> CodeFormat:
        """Return the code format."""
        return CodeFormat.NUMBER

    @property
    def code_arm_required(self) -> bool:
        """Return if code is required for arming."""
        return True

    @property
    def state(self) -> AlarmControlPanelState | None:
        """Return the state of the device."""
        if not self.coordinator.data or "mode" not in self.coordinator.data:
            return None

        # Get mode data from coordinator
        mode_response = self.coordinator.data["mode"]
        areas = mode_response.get("data", [])

        # Find the area matching our area_id
        for area in areas:
            if str(area.get("area")) == str(self._area_id):
                mode = area.get("mode", "").lower()

                # Map API mode to Home Assistant state
                if mode == "arm":
                    return AlarmControlPanelState.ARMED_AWAY
                elif mode in ["home", "home_1", "home_2", "home_3"]:
                    return AlarmControlPanelState.ARMED_HOME
                elif mode == "disarm":
                    return AlarmControlPanelState.DISARMED

                _LOGGER.debug("Unknown mode '%s' for area %s", mode, self._area_id)

        return None

    async def async_alarm_disarm(self, code: str | None = None) -> None:
        """Send disarm command."""
        if code:
            try:
                await self._api.set_panel_mode(self._area_id, MODE_DISARM, code)
                await self.coordinator.async_request_refresh()
            except Exception as err:
                _LOGGER.error("Failed to disarm: %s", err)

    async def async_alarm_arm_home(self, code: str | None = None) -> None:
        """Send arm home command."""
        if code:
            try:
                await self._api.set_panel_mode(self._area_id, MODE_HOME, code)
                await self.coordinator.async_request_refresh()
            except Exception as err:
                _LOGGER.error("Failed to arm home: %s", err)

    async def async_alarm_arm_away(self, code: str | None = None) -> None:
        """Send arm away command."""
        if code:
            try:
                await self._api.set_panel_mode(self._area_id, MODE_ARM, code)
                await self.coordinator.async_request_refresh()
            except Exception as err:
                _LOGGER.error("Failed to arm away: %s", err)
