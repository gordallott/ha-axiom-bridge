""" config flow for axiom integration """

from typing import Any
from homeassistant import config_entries, data_entry_flow
import voluptuous as vol
from .const import DOMAIN


@config_entries.HANDLERS.register(DOMAIN)
class AxiomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Axiom config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        return self.async_show_form(
            step_id="user",
            data_schema=({vol.Required("APIKey"): str, vol.Required("dataset"): str}),
        )
