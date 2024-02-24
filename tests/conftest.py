import os
import pprint

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
    os.environ = {
        key: value
        for key, value in os.environ.items()
        if key not in ["PIWIK_URL", "PIWIK_AUTH_URL", "PIWIK_CLIENT_ID", "PIWIK_CLIENT_SECRET"]
    }
    return mock.patch.dict(os.environ, envvars)


@pytest.fixture
def adapter():
    yield requests_mock.Mocker()


@pytest.fixture
def adapter_token(adapter: requests_mock.Mocker):
    adapter.register_uri(
        "POST",
        PIWIK_AUTH_URL,
        json=PIWIK_TOKEN,
        status_code=200,
    )

    yield adapter


@pytest.fixture
def base_client(adapter_token: requests_mock.Mocker):
    with adapter_token:
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
def client(adapter_token: requests_mock.Mocker):
    with adapter_token:
        client = Client(
            url=PIWIK_URL,
            auth_url=PIWIK_AUTH_URL,
            client_id=PIWIK_CLIENT_ID,
            client_secret=PIWIK_CLIENT_SECRET,
        )
        yield client
        client._token_storage.clear_cache()
