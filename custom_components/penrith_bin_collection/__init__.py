from homeassistant import core
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN


CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

async def async_setup(hass: core.HomeAssistant, config: dict) -> bool:
    """Set up the Penrith Bin Collection component."""
    # @TODO: Add setup code.
    return True
