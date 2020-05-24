# -*- coding: utf-8 -*-
import logging

import requests

from six.moves.urllib.parse import urljoin
import ckan.plugins.toolkit as tk

log = logging.getLogger(__name__)


def get_actions():
    return {
        'fpx_order_ticket': fpx_order_ticket,
    }

def fpx_order_ticket(context, data_dict):
    type_, items = tk.get_or_bust(data_dict, ['type', 'items'])
    if not items:
        raise tk.ValidationError({'items': ['Cannot be empty']})
    tk.check_access('fpx_order_ticket', context, data_dict)
    url = urljoin(tk.h.fpx_service_url(), '/ticket/generate')
    data = {
        'type': type_,
        'items': items
    }

    headers = {}
    secret = tk.h.fpx_client_secret()
    if secret:
        headers['authorize'] = secret

    resp = requests.post(url, json=data, headers=headers)
    return resp.json()
