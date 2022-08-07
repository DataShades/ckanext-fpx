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
    url = urljoin(tk.h.fpx_service_url(), "ticket/generate")
    type_ = data_dict["type"]
    items = data_dict["items"]
    options = data_dict.get("options", {})

    if type_ == "package":
        type_ = "url"
        if not isinstance(items, list):
            log.warning(
                "Passing items as scalar value when type set to 'package' is "
                "deprecated. Use list instead."
            )
            items = [items]

        fq_list = [
            "{!q.op=OR}id:(%s)"
            % " ".join(['"{}"'.format(item) for item in items])
        ]
        result = tk.get_action("package_search")(
            None, {"fq_list": fq_list, "include_private": True}
        )

        items = [
            {"url": r["url"], "path": pkg["name"]}
            for pkg in result["results"]
            for r in pkg["resources"]
        ]

    elif type_ == "resource":
        type_ = "url"
        items = [
            tk.get_action("resource_show")(None, {"id": r["id"]})["url"]
            for r in items
        ]

    items = [
        item if isinstance(item, dict) else dict(url=item) for item in items
    ]

    try:
        user = tk.get_action("user_show")(None, {"id": context["user"]})
    except tk.ObjectNotFound:
        user = None

    if user:
        if not user["apikey"]:
            log.info("Generating API Key for user %s", user["name"])
            user = tk.get_action("user_generate_apikey")(
                {}, {"id": user["id"]}
            )

        headers = {"Authorization": user["apikey"]}
        for item in items:
            if not tk.h.url_is_local(item["url"]):
                continue
            item.setdefault("headers", {}).update(headers)

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
