# -*- coding: utf-8 -*-
import logging
import json
import base64
import requests

from urllib.parse import urljoin
from ckan.lib import redis
import ckan.plugins.toolkit as tk
from ckan.logic import validate

from . import schema
from .. import utils

log = logging.getLogger(__name__)


def get_actions():
    return {
        "fpx_order_ticket": order_ticket,
    }


def _get_token(name):
    """Return API token for username
    """
    conn = redis.connect_to_redis()
    key = f"fpx:token:{name}"
    token = conn.get(key)

    if not token:
        log.info("Generating API Token for user %s", name)
        token = tk.get_action("api_token_create")(
            {"user": name}, {"user": name, "name": "File downloads"}
        )["token"]
        conn.set(key, token)
    else:
        token = token.decode()

    return token

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
    except (tk.ObjectNotFound, tk.NotAuthorized):
        user = None

    if user:
        token = _get_token(user["name"])

        headers = {"Authorization": token}
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
