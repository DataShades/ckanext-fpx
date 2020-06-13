import pytest

import ckan.plugins.toolkit as tk

from ckan.exceptions import CkanConfigurationException


class TestFpxServiceUrl(object):
    def test_url_is_missing(self):
        with pytest.raises(CkanConfigurationException):
            tk.h.fpx_service_url()

    @pytest.mark.ckan_config('fpx.service.url', 'http://fpx.service:8000/')
    def test_url_is_specified(self):
        assert tk.h.fpx_service_url() == 'http://fpx.service:8000/'

    @pytest.mark.ckan_config('fpx.service.url', 'http://fpx.service:8000')
    def test_url_ends_with_slash(self):
        assert tk.h.fpx_service_url() == 'http://fpx.service:8000/'


class TestFpxClientSecret(object):
    def test_secret_is_missing(self):
        assert tk.h.fpx_client_secret() is None

    @pytest.mark.ckan_config('fpx.client.secret', '123')
    def test_secret_is_specified(self):
        assert tk.h.fpx_client_secret() == '123'
