# -*- coding: utf-8 -*-
import logging
import json
import base64
import requests

from urllib.parse import urljoin

import ckan.plugins.toolkit as tk
from ckan.logic import validate

from . import schema
from .. import utils

log = logging.getLogger(__name__)


def get_actions():
    return {
        "fpx_order_ticket": order_ticket,
    }


@validate(schema.order_ticket)
def order_ticket(context, data_dict):
    tk.check_access("fpx_order_ticket", context, data_dict)
    url = urljoin(tk.h.fpx_service_url(internal=True), "ticket/generate")
    type_ = data_dict["type"]
    items = data_dict["items"]
    options = data_dict.get("options", {})

    normalizer = utils.get_normalizer()

    items, type_ = normalizer.fpx_normalize_items_and_type(items, type_)

    try:
        user = tk.get_action("user_show")(
            context.copy(), {"id": context["user"]}
        )
    except tk.ObjectNotFound:
        user = None

    if user:
        if not user["apikey"]:
            log.info("Generating API Key for user %s", user["name"])
            user = tk.get_action("user_generate_apikey")(
                context.copy(), {"id": user["id"]}
            )

        headers = {"Authorization": user["apikey"]}
        for item in items:
            if not tk.h.url_is_local(item["url"]):
                continue
            item.setdefault("headers", {}).update(headers)

    if type_ == "url":
        log.warning(
            "`url` type of FPX tickets is deprecated. Use `zip` instead"
        )
        type_ = "zip"

    data = {
        "type": type_,
        "items": base64.encodebytes(bytes(json.dumps(items), "utf8")),
        "options": base64.encodebytes(bytes(json.dumps(options), "utf8")),
    }
    headers = {}
    secret = utils.client_secret()
    if secret:
        headers["authorize"] = secret

    resp = requests.post(url, json=data, headers=headers)
    if resp.ok:
        return resp.json()

    try:
        errors = resp.json()
    except ValueError:
        log.exception(f"FPX ticket order: {resp.content}")
        raise


    raise tk.ValidationError(errors)
