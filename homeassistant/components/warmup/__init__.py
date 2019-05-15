"""The warmup component."""
import logging


from .config_flow import WarmupFlowHandler  # noqa: pylint: disable=unused-import

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    """Set up the Warmup Component."""
    return True


async def async_setup_entry(hass, config_entry):
    """Set up Warmup from a config entry."""
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(
        config_entry, 'climate'))
    return True


async def async_unload_entry(hass, entry):
    """Unload a Warmup config entry."""
    await hass.config_entries.async_forward_entry_unload(
        entry, 'climate')
    return True