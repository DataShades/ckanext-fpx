# -*- coding: utf-8 -*-

from ckan.exceptions import CkanConfigurationException

import ckan.plugins.toolkit as tk

_service_url_key = "fpx.service.url"
_client_secret_key = "fpx.client.secret"


def get_helpers():
    return {
        "fpx_service_url": fpx_service_url,
        "fpx_client_secret": fpx_client_secret,
    }


def fpx_service_url():
    url = tk.config.get(_service_url_key)
    if not url:
        raise CkanConfigurationException(
            "Missing `{}`".format(_service_url_key)
        )
    return url.rstrip('/') + '/'


def fpx_client_secret():
    return tk.config.get(_client_secret_key)
