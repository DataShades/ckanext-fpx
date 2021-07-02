import pytest
import ckan.plugins as p


@pytest.mark.usefixtures("with_plugins")
def test_plugin_loaded():
    assert p.plugin_loaded("fpx")
