"""Penrith Bin Collection sensor platform."""
import logging
import re
from datetime import timedelta
from typing import Any, Callable, Dict, Optional
from urllib import parse


import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import (
    ATTR_NAME,
    CONF_ACCESS_TOKEN,
    CONF_NAME,
    CONF_PATH,
    CONF_URL,
)
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.typing import (
    ConfigType,
    DiscoveryInfoType,
    HomeAssistantType,
)

from .const import (
    WEBSITE_URL,
    ATTR_HOME_LOCALITY,
    ATTR_HOME_STREET,
    ATTR_HOME_PROPERTY,
    ATTR_NEXT_WASTE_COLLECTION
)

from .penrith_bin_collection import get_localities, get_street, get_properties, get_calender, find_locality, find_street, find_property

_LOGGER = logging.getLogger(__name__)
# Time between updating data from GitHub
SCAN_INTERVAL = timedelta(minutes=10)

CONF_REPOS = "repositories"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ACCESS_TOKEN): cv.string
    }
)

LINK_RE = re.compile(
    r"\<(?P<uri>[^>]+)\>;\s*" r'(?P<param_type>\w+)="(?P<param_value>\w+)"(,\s*)?'
)

async def async_setup_entry(
    hass: core.HomeAssistant,
    config_entry: config_entries.ConfigEntry,
    async_add_entities,
):
    """Setup sensors from a config entry created in the integrations UI."""
    config = hass.data[DOMAIN][config_entry.entry_id]
    session = async_get_clientsession(hass)
    sensors = [NextWasteCollectionSensor()]
    async_add_entities(sensors, update_before_add=True)


async def async_setup_platform(
    hass: HomeAssistantType,
    config: ConfigType,
    async_add_entities: Callable,
    discovery_info: Optional[DiscoveryInfoType] = None,
) -> None:
    """Set up the sensor platform."""
    session = async_get_clientsession(hass)
    sensors = [NextWasteCollectionSensor()]
    async_add_entities(sensors, update_before_add=True)


class NextWasteCollectionSensor(Entity):
    """Representation of a GitHub Repo sensor."""

    def __init__(self):
        super().__init__()
        self.attrs: Dict[str, Any] = {ATTR_PATH: self.repo}
        self._name = repo.get("name", self.repo)
        self._state = None
        self._available = True

    @property
    def name(self) -> str:
        """Return the name of the entity."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return the unique ID of the sensor."""
        return "next_waste_bin_collection"

    @property
    def available(self) -> bool:
        """Return True if entity is available."""
        return self._available

    @property
    def state(self) -> Optional[str]:
        return self._state

    @property
    def device_state_attributes(self) -> Dict[str, Any]:
        return self.attrs

    async def async_update(self):
        localities = get_localities()
        
        selected_locality = find_locality(localities, ATTR_HOME_LOCALITY)
        selected_locality_id = selected_locality["id"]
        
        streets = get_street(selected_locality_id)
        
        selected_street = find_street(streets, ATTR_HOME_STREET)
        selected_street_id = selected_street["id"]
        
        properties = get_properties(selected_street_id)
        selected_property = find_property(properties, ATTR_HOME_PROPERTY)
        selected_property_id = selected_property["id"]
        
        calendar = get_calendar(selected_property_id)
        
        for event in calendar[EVENT_TYPE.Waste.value]:
            self.attrs[ATTR_NEXT_WASTE_COLLECTION] = event["dow"][0]

            # for event in calendar[EVENT_TYPE.Recycle.value]:
            #     pprint_event(event)

            # for event in calendar[EVENT_TYPE.Special.value]:
            #     print(event)
