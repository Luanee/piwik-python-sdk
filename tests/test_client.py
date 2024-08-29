from piwik.base import BaseClient
from piwik.client import Client
from tests.conftest import PIWIK_URL


def test_base_client_initialization(base_client: BaseClient):
    assert base_client._config.url == PIWIK_URL


def test_client_initialization(client: Client):
    assert client._config.url == PIWIK_URL
