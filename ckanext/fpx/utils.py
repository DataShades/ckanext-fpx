import logging
import ckan.plugins.toolkit as tk
from ckan.plugins import PluginImplementations
from . import interfaces

log = logging.getLogger(__name__)

CONFIG_SECRET_LEGACY = "ckanext.fpx.client.secret"
CONFIG_SECRET = "fpx.client.secret"

CONFIG_NAME = "fpx.client.name"


def client_secret():
    secret = tk.config.get(CONFIG_SECRET)
    if not secret:
        secret = tk.config.get(CONFIG_SECRET_LEGACY)
        if secret:
            log.warning(
                "Config option `%s` is deprecated. Use `%s` instead",
                CONFIG_SECRET_LEGACY,
                CONFIG_SECRET,
            )

    return secret


def client_name():
    return tk.config.get(CONFIG_NAME)


def get_normalizer() -> interfaces.IFpx:
    """Return normalizer for FPX payload.

    The first plugins that implements IFpx interface will be used as normalizer.
    """
    return next(iter(PluginImplementations(interfaces.IFpx)))
