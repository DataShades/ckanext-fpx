import pytest
from ckanext.fpx import utils


@pytest.mark.usefixtures("with_plugins")
class TestFpxClientSecret(object):
    def test_secret_is_missing(self):
        assert utils.client_secret() is None

    @pytest.mark.ckan_config(utils.CONFIG_SECRET_LEGACY, "123")
    def test_legacy_secret_is_specified(self):
        assert utils.client_secret() == "123"

    @pytest.mark.ckan_config(utils.CONFIG_SECRET, "123")
    def test_secret_is_specified(self):
        assert utils.client_secret() == "123"
