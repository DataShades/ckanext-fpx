# -*- coding: utf-8 -*-
import logging
import json
import base64
import requests
import six

from six.moves.urllib.parse import urljoin
import ckan.plugins.toolkit as tk
from ckan.exceptions import CkanException

log = logging.getLogger(__name__)


def get_actions():
    return {
        "fpx_order_ticket": fpx_order_ticket,
    }


def fpx_order_ticket(context, data_dict):
    type_ = tk.get_or_bust(data_dict, "type")
    items = data_dict.get("items", '')
    if not items:
        raise tk.ValidationError({"items": ["Cannot be empty"]})
    try:
        items = json.loads(base64.decodestring(six.ensure_binary(items)))
    except ValueError:
        raise tk.ValidationError({"items": ["Must be a base64-decoded JSON-string"]})

    tk.check_access("fpx_order_ticket", context, data_dict)
    url = urljoin(tk.h.fpx_service_url(), "ticket/generate")
    if type_ == "package":
        type_ = "url"
        if not isinstance(items, list):
            log.warning(
                "Passing items as scalar value when type set to 'package' is "
                "deprecated. Use list instead."
            )
            items = [items]
        fq_list = ["{!q.op=OR}id:(%s)" % " ".join([
            '"{}"'.format(item)
            for item in items
        ])]
        result = tk.get_action("package_search")(
            None, {"fq_list": fq_list, "include_private": True}
        )

        items = [
            {"url": r["url"], "path": pkg["name"]}
            for pkg in result['results']
            for r in pkg["resources"]
        ]
    elif type_ == "resource":
        type_ = "url"
        items = [
            tk.get_action("resource_show")(None, {"id": r["id"]})["url"]
            for r in items
        ]
    items = [
        item if isinstance(item, dict) else dict(url=item)
        for item in items
    ]
    try:
        user = tk.get_action('user_show')(None, {'id': context['user']})
    except tk.ObjectNotFound:
        user = None
    if user:
        headers = {'Authorization': user['apikey']}
        for item in items:
            item.setdefault('headers', {}).update(headers)
    data = {"type": type_, "items": base64.encodestring(six.ensure_binary(json.dumps(items)))}

    headers = {}
    secret = tk.h.fpx_client_secret()
    if secret:
        headers["authorize"] = secret

    resp = requests.post(url, json=data, headers=headers)
    if not resp.ok:
        try:
            raise tk.ValidationError(resp.json())
        except ValueError:
            log.exception("FPX ticket order")
            raise

    return resp.json()
