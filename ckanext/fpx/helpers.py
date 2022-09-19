from __future__ import annotations

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
CONFIG_INTERNAL_URL = "fpx.service.internal_url"
CONFIG_NO_QUEUE = "fpx.service.no_queue"

DEFAULT_NO_QUEUE = True


def get_helpers():
    return {
        "fpx_service_url": fpx_service_url,
        "fpx_into_stream_url": fpx_into_stream_url,
        "fpx_no_queue": fpx_no_queue,
    }


def fpx_no_queue() -> bool:
    """Start downloads immediately, without waiting in queue.

    Requires FPX service running with `FPX_NO_QUEUE = True` option(default from
    v0.4.0).

    """
    return tk.asbool(tk.config.get(CONFIG_NO_QUEUE, DEFAULT_NO_QUEUE))


def fpx_service_url(*, internal: bool = False) -> str:
    f"""Return the URL of FPX service.

    Keyword Args:

        internal(optional): make an attempt to return value of
        `{CONFIG_INTERNAL_URL}` option. This feature can be used internally(for
        ticket ordering) in order to bypass load-balancer and access FPX
        service directly. When `{CONFIG_INTERNAL_URL}` is empty, normal
        URL(`{CONFIG_URL}`) is returned instead.

    """
    url = tk.config.get(CONFIG_URL)
    if not url:
        url = tk.config.get(CONFIG_URL_LEGACY)
        if url:
            log.warning(
                "Config option `%s` is deprecated. Use `%s` instead",
                CONFIG_URL_LEGACY,
                CONFIG_URL,
            )

    if internal:
        internal_url = tk.config.get(CONFIG_INTERNAL_URL)
        if internal_url:
            log.debug("Switching to internal URL")
            url = internal_url

    if not url:
        raise CkanConfigurationException("Missing `{}`".format(CONFIG_URL))
    return url.rstrip("/") + "/"


def fpx_into_stream_url(url: str) -> Optional[str]:
    """Turn arbitrary link into URL to downloadable stream.

    In this way any URL that is accessible only from FPX service can be proxied
    to the client through FPX.

    Args:
        url: Download URL

    Returns:
        URL to the FPX endpoint that streams content from the Download URL.
        None, if client's name or secret are missing.

    """
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
