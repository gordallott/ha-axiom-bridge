"""Custom integration to integrate integration_blueprint with Home Assistant.

For more details about this integration, please refer to
https://github.com/ludeeus/integration_blueprint
"""
from __future__ import annotations
import logging
import datetime

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant import core as hacore
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.const import (
    ATTR_BATTERY_LEVEL,
    ATTR_DEVICE_CLASS,
    ATTR_FRIENDLY_NAME,
    ATTR_MODE,
    ATTR_TEMPERATURE,
    ATTR_UNIT_OF_MEASUREMENT,
    CONTENT_TYPE_TEXT_PLAIN,
    EVENT_STATE_CHANGED,
    PERCENTAGE,
    STATE_CLOSED,
    STATE_CLOSING,
    STATE_ON,
    STATE_OPEN,
    STATE_OPENING,
    STATE_UNAVAILABLE,
    STATE_UNKNOWN,
    UnitOfTemperature,
)
from homeassistant.helpers.entity_registry import EVENT_ENTITY_REGISTRY_UPDATED
import axiom

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.SWITCH,
]

# xaat-ea1f991b-a7c5-4d11-a09c-6cf8d94c6f9c


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
def setup(hass: HomeAssistant, conf: ConfigEntry) -> bool:
    """Set up this integration using UI."""
    _LOGGER.debug("setup called, config: %s", conf.data)
    # metrics = AxiomMetrics(conf.data["APIKey"], conf.data["dataset"])
    # hass.bus.listen(EVENT_STATE_CHANGED, metrics.handle_state_changed)
    return True


class AxiomMetrics:
    """handles and exports metrics from home assistant to Axiom"""

    def __init__(self, apikey, dataset):
        """Initialize."""
        self.dataset = dataset
        self.client = axiom.Client(token=apikey)

    def handle_state_changed(self, event):
        """Listen for new messages on the bus, and add them to Axiom."""
        if (state := event.data.get("new_state")) is None:
            return

        entity_id = state.entity_id
        _LOGGER.debug("Handling state update for %s", entity_id)
        # TODO: filtering

        self.client.ingest_events(
            dataset=self.dataset,
            events=[
                {entity_id: state.state},
            ],
        )
