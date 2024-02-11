import os

from typing import cast
from unittest import mock

import pytest
import requests_mock

from piwik.base import BaseClient
from piwik.base.token import DefaultTokenStorage
from piwik.client import Client


PIWIK_URL = "https://test.piwik.pro"
PIWIK_AUTH_URL = "https://test.piwik.pro/auth/token"
PIWIK_CLIENT_ID = "test_client_id"
PIWIK_CLIENT_SECRET = "test_client_secret"

PIWIK_TOKEN = {
    "access_token": "token",
}


def environment(**envvars):
    return mock.patch.dict(os.environ, envvars)


@pytest.fixture
def requests_mocker():
    mocker = requests_mock.Mocker()
    mocker.register_uri(
        "POST",
        PIWIK_AUTH_URL,
        json=PIWIK_TOKEN,
        status_code=200,
    )

    yield mocker


@pytest.fixture
def base_client(requests_mocker):
    with requests_mocker:

        token_storage = DefaultTokenStorage()
        token_storage.add_token(PIWIK_CLIENT_ID, PIWIK_TOKEN)

        client = BaseClient(
            url=PIWIK_URL,
            auth_url=PIWIK_AUTH_URL,
            client_id=PIWIK_CLIENT_ID,
            client_secret=PIWIK_CLIENT_SECRET,
        )
        yield client
        client._token_storage.clear_cache()


@pytest.fixture
def client(requests_mocker):
    with requests_mocker:
        client = Client(
            url=PIWIK_URL,
            auth_url=PIWIK_AUTH_URL,
            client_id=PIWIK_CLIENT_ID,
            client_secret=PIWIK_CLIENT_SECRET,
        )
        yield client
        client._token_storage.clear_cache()
