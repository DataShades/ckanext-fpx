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
        helpers.CONFIG_URL_LEGASY, "http://fpx.service:8000/"
    )
    def test_legacy_url_is_specified(self):
        assert tk.h.fpx_service_url() == "http://fpx.service:8000/"

    @pytest.mark.ckan_config(
        helpers.CONFIG_URL_LEGASY, "http://fpx.service:8000"
    )
    def test_legacy_url_ends_with_slash(self):
        assert tk.h.fpx_service_url() == "http://fpx.service:8000/"

    @pytest.mark.ckan_config(helpers.CONFIG_URL, "http://fpx.service:8000/")
    def test_url_is_specified(self):
        assert tk.h.fpx_service_url() == "http://fpx.service:8000/"

    @pytest.mark.ckan_config(helpers.CONFIG_URL, "http://fpx.service:8000")
    def test_url_ends_with_slash(self):
        assert tk.h.fpx_service_url() == "http://fpx.service:8000/"


@pytest.mark.usefixtures("with_plugins")
class TestFpxClientSecret(object):
    def test_secret_is_missing(self):
        assert tk.h.fpx_client_secret() is None

    @pytest.mark.ckan_config(helpers.CONFIG_SECRET_LEGACY, "123")
    def test_legacy_secret_is_specified(self):
        assert tk.h.fpx_client_secret() == "123"

    @pytest.mark.ckan_config(helpers.CONFIG_SECRET, "123")
    def test_secret_is_specified(self):
        assert tk.h.fpx_client_secret() == "123"
