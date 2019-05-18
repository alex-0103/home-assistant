"""Config flow to configure warmup component."""
from collections import OrderedDict
from typing import Optional

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.helpers import ConfigType
from homeassistant.components.warmup.const import DEFAULT_TITLE


@config_entries.HANDLERS.register('warmup')
class WarmupFlowHandler(config_entries.ConfigFlow):
    """Handle a warmup config flow."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize flow."""
        self._username = None  # type: Optional[str]
        self._password = None  # type: Optional[str]
        #self._location = None  # type: Optional[str]
        #self._room = None  # type: Optional[str]
        #self._name = None  # type: Optional[str]
        #self._target_temp = None  # type: Optional[str]

    async def async_step_user(self, user_input: Optional[ConfigType] = None,
                              error: Optional[str] = None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            return await self._async_add(user_input)

        fields = OrderedDict()
        fields[vol.Required('username', default=self._username or vol.UNDEFINED)] = str
        fields[vol.Required('password', default=self._password or vol.UNDEFINED)] = str
        #fields[vol.Required('location', default=self._location or vol.UNDEFINED)] = str
        #fields[vol.Required('room', default=self._room or vol.UNDEFINED)] = str
        #fields[vol.Optional('name', default=self._name or 'Warmup4IE')] = str
        #fields[vol.Optional('target_temp', default=self._target_temp or 20)] = int

        errors = {}
        if error is not None:
            errors['base'] = error

        return self.async_show_form(
            step_id='user',
            data_schema=vol.Schema(fields),
            errors=errors
        )

    async def _async_add(self, user_input,
                                         from_discovery=False):

        self._username = user_input['username']
        self._password = user_input['password']
        #self._location = user_input['location']
        #self._room = user_input['room']
        #self._name = user_input['name']
        #self._target_temp = user_input['target_temp']
        error = await self.fetch_device_info()
        if error is not None:
            return await self.async_step_user(error=error)
        #if not self._name:
        #    self._name = 'warmup'

        return self._async_get_entry()




    def _async_get_entry(self):
        return self.async_create_entry(
            title=DEFAULT_TITLE,
            data={
            'username' : self._username,
            'password' : self._password
            }
        )


    async def fetch_device_info(self):
        """Fetch device info from API and return any errors."""
        from warmup4ie import Warmup4IEDevice
        device = Warmup4IEDevice(self._username, self._password)
        if device is None or not device.setup_finished:
            return 'connection_error'

        return None

