import logging
from typing import Any, Dict, Optional

from gidgethub import BadRequest
from gidgethub.aiohttp import GitHubAPI
from homeassistant import config_entries, core
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_NAME, CONF_PATH, CONF_URL
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import CONF_REPOS, DOMAIN

_LOGGER = logging.getLogger(__name__)

class PenrithBinCollectionCustomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Penrith Bin Collection Custom config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_location(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        errors: Dict[str, str] = {}
        return self.async_create_entry(title="AGL Energy", data=self.data)
