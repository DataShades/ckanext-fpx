import os
import logging

from typing import Optional

import jwt

from ckan.exceptions import CkanConfigurationException

import ckan.plugins.toolkit as tk
from . import utils

log = logging.getLogger(__name__)

CONFIG_URL_LEGACY = "ckanext.fpx.service.url"
CONFIG_URL = "fpx.service.url"


def get_helpers():
    return {
        "fpx_service_url": fpx_service_url,
        "fpx_into_stream_url": fpx_into_stream_url,
    }


def fpx_service_url():
    url = tk.config.get(CONFIG_URL)
    if not url:
        url = tk.config.get(CONFIG_URL_LEGACY)
        if url:
            log.warning(
                "Config option `%s` is deprecated. Use `%s` instead",
                CONFIG_URL_LEGACY,
                CONFIG_URL,
            )

    if not url:
        raise CkanConfigurationException("Missing `{}`".format(CONFIG_URL))
    return url.rstrip("/") + "/"


def fpx_into_stream_url(url: str) -> Optional[str]:
    name = utils.client_name()
    secret = utils.client_secret()

    if not name or not secret:
        log.debug(
            "Do not generate stream URL because client details are incomplete"
        )
        return

    filename = os.path.basename(url.rstrip("/"))
    encoded = jwt.encode(
        {
            "url": url,
            "response_headers": {
                "content-disposition": f'attachment; filename="{filename}"'
            },
        },
        secret,
        algorithm="HS256",
    ).decode("utf8")
    service = tk.h.fpx_service_url()
    url = f"{service}stream/url/{encoded}?client={name}"

    return url
