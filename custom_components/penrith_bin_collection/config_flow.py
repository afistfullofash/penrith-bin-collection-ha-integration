import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries, core
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_NAME, CONF_PATH, CONF_URL
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import CONF_REPOS, DOMAIN

_LOGGER = logging.getLogger(__name__)

class PenrithBinCollectionConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Penrith Bin Collection Custom config flow."""
    VERSION = 1
    MINOR_VERSION = 1
    async def async_step_user(self, info):
        """Invoked when a user initiates a flow via the user interface."""
        if info is not None:
            pass  # TODO: process info

        schema = vol.Schema({})
        return self.async_show_form(step_id="user", data=schema)
