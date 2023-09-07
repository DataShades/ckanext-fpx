from __future__ import annotations
import base64
import json
from flask import Blueprint
import ckan.plugins.toolkit as tk

from . import utils


def get_blueprints():
    return [fpx]


fpx = Blueprint("fpx", __name__)


@fpx.route("/dataset/<id>/resource/<resource_id>/fpx")
def resource_download(id: str, resource_id: str):
    normalizer = utils.get_normalizer()

    try:
        res = tk.get_action("resource_show")({}, {"id": resource_id})
        ticket = tk.get_action("fpx_order_ticket")(
            {},
            {
                "type": "stream",
                "items": [normalizer.fpx_url_from_resource(res)],
            },
        )
    except (tk.NotAuthorized, tk.ObjectNotFound):
        return tk.abort(404, tk._("Not found"))

    id_ = ticket["id"]

    return tk.redirect_to(tk.h.fpx_service_url() + f"ticket/{id_}/download")


@fpx.route("/dataset/<id>/fpx")
def package_download(id: str):
    normalizer = utils.get_normalizer()

    try:
        pkg = tk.get_action("package_show")({}, {"id": id})
        items = normalizer.fpx_normalize_items_and_type([pkg["id"]], "package")[0]
    except (tk.NotAuthorized, tk.ObjectNotFound):
        return tk.abort(404, tk._("Not found"))

    ticket = tk.get_action("fpx_order_ticket")(
        {},
        {
            "type": "zip",
            "items": base64.encodebytes(json.dumps(items).encode()).decode(),
        },
    )

    id_ = ticket["id"]

    return tk.redirect_to(tk.h.fpx_service_url() + f"ticket/{id_}/download")
