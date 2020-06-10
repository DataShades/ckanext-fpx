# -*- coding: utf-8 -*-
import logging

import requests

from six.moves.urllib.parse import urljoin
import ckan.plugins.toolkit as tk
from ckan.exceptions import CkanException

log = logging.getLogger(__name__)


def get_actions():
    return {
        'fpx_order_ticket': fpx_order_ticket,
    }

def fpx_order_ticket(context, data_dict):
    type_ = tk.get_or_bust(data_dict, 'type')
    items = data_dict.get('items', [])
    if not items:
        raise tk.ValidationError({'items': ['Cannot be empty']})
    tk.check_access('fpx_order_ticket', context, data_dict)
    url = urljoin(tk.h.fpx_service_url(), 'ticket/generate')
    if type_ == 'package':
        type_ = 'url'
        pkg = tk.get_action('package_show')(None, {'id': items})
        items = [{
            "url": r['url'],
            "path": pkg['name']
        } for r in pkg['resources']]
    elif type_ == 'resource':
        type_ = 'url'
        items = [
            tk.get_action('resource_show')(None, {'id': r['id']})['url']
            for r in items
        ]

    data = {
        'type': type_,
        'items': items
    }

    headers = {}
    secret = tk.h.fpx_client_secret()
    if secret:
        headers['authorize'] = secret

    resp = requests.post(url, json=data, headers=headers)
    if not resp.ok:
        try:
            raise tk.ValidationError(resp.json())
        except ValueError:
            log.exception("FPX ticket order")
            raise

    return resp.json()
