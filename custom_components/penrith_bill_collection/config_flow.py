import logging
from typing import Any, Dict, Optional

from homeassistant import config_entries

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class PenrithBinCollectionCustomConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Github Custom config flow."""

    data: Optional[Dict[str, Any]]

    async def async_step_location(self, user_input: Optional[Dict[str, Any]] = None):
        """Invoked when a user initiates a flow via the user interface."""
        return self.async_create_entry(title="Penrith Bill Collection", data=self.data)
