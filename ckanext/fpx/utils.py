import logging
import ckan.plugins.toolkit as tk


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
