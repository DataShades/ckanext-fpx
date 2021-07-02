import pytest

import ckan.plugins.toolkit as tk
from ckan.tests.helpers import call_action

import ckanext.fpx.helpers as h


@pytest.mark.usefixtures("with_plugins")
@pytest.mark.ckan_config(h.CONFIG_URL, "http://fpx")
class TestOrderTicket:
    @pytest.mark.parametrize(
        "payload", [{}, {"type": "package"}, {"items": []}, {"items": "hello"}]
    )
    def test_validation(self, payload):
        with pytest.raises(tk.ValidationError):
            call_action("fpx_order_ticket", **payload)
