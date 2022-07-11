import pytest

import ckan.plugins.toolkit as tk

from ckan.exceptions import CkanConfigurationException
import ckanext.fpx.helpers as helpers


@pytest.mark.usefixtures("with_plugins")
class TestFpxServiceUrl(object):
    def test_url_is_missing(self):
        with pytest.raises(CkanConfigurationException):
            tk.h.fpx_service_url()

    @pytest.mark.ckan_config(
        helpers.CONFIG_URL_LEGACY, "http://fpx.service:8000/"
    )
    def test_legacy_url_is_specified(self):
        assert tk.h.fpx_service_url() == "http://fpx.service:8000/"

    @pytest.mark.ckan_config(
        helpers.CONFIG_URL_LEGACY, "http://fpx.service:8000"
    )
    def test_legacy_url_ends_with_slash(self):
        assert tk.h.fpx_service_url() == "http://fpx.service:8000/"

    @pytest.mark.ckan_config(helpers.CONFIG_URL, "http://fpx.service:8000/")
    def test_url_is_specified(self):
        assert tk.h.fpx_service_url() == "http://fpx.service:8000/"

    @pytest.mark.ckan_config(helpers.CONFIG_URL, "http://fpx.service:8000")
    def test_url_ends_with_slash(self):
        assert tk.h.fpx_service_url() == "http://fpx.service:8000/"
