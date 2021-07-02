# -*- coding: utf-8 -*-

from ckan.exceptions import CkanConfigurationException

import ckan.plugins.toolkit as tk

CONFIG_URL = "ckanext.fpx.service.url"
CONFIG_URL_LEGASY = "fpx.service.url"

CONFIG_SECRET = "ckanext.fpx.client.secret"
CONFIG_SECRET_LEGACY = "fpx.client.secret"


def get_helpers():
    return {
        "fpx_service_url": fpx_service_url,
        "fpx_client_secret": fpx_client_secret,
    }


def fpx_service_url():
    url = tk.config.get(CONFIG_URL) or tk.config.get(CONFIG_URL_LEGASY)

    if not url:
        raise CkanConfigurationException("Missing `{}`".format(CONFIG_URL))
    return url.rstrip("/") + "/"


def fpx_client_secret():
    return tk.config.get(CONFIG_SECRET) or tk.config.get(CONFIG_SECRET_LEGACY)
