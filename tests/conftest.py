import os
from typing import Optional
from unittest import mock

import pytest
import requests_mock
from pytest import FixtureRequest

from piwik.base import BaseClient
from piwik.base.config import ClientConfig
from piwik.base.token import DefaultTokenStorage
from piwik.client import Client

PIWIK_URL = "https://test.piwik.pro"
PIWIK_AUTH_URL = "https://test.piwik.pro/auth/token"
PIWIK_CLIENT_ID = "test_client_id"
PIWIK_CLIENT_SECRET = "test_client_secret"

PIWIK_TOKEN = {
    "access_token": "token",
}


@pytest.fixture
def config(
    url: Optional[str] = None,
    auth_url: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
):
    yield ClientConfig(
        url=url or PIWIK_URL,
        auth_url=auth_url or PIWIK_AUTH_URL,
        client_id=client_id or PIWIK_CLIENT_ID,
        client_secret=client_secret or PIWIK_CLIENT_SECRET,  # type: ignore
    )


@pytest.fixture
def environment(request: FixtureRequest):
    os.environ = {
        key: value
        for key, value in os.environ.items()
        if key
        not in [
            "PIWIK_URL",
            "PIWIK_AUTH_URL",
            "PIWIK_CLIENT_ID",
            "PIWIK_CLIENT_SECRET",
        ]
    }

    env_vars_to_patch = getattr(request, "param", {})
    yield mock.patch.dict(os.environ, env_vars_to_patch)


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
def base_client(config: ClientConfig, adapter_token: requests_mock.Mocker):
    with adapter_token:
        token_storage = DefaultTokenStorage()
        token_storage.add_token(PIWIK_CLIENT_ID, PIWIK_TOKEN)

        client = BaseClient(
            url=config.url,
            auth_url=config.auth_url,
            client_id=config.client_id,
            client_secret=config.client_secret,
        )
        yield client
        client._token_storage.clear_cache()


@pytest.fixture
def client(config: ClientConfig, adapter_token: requests_mock.Mocker):
    with adapter_token:
        client = Client(
            url=config.url,
            auth_url=config.auth_url,
            client_id=config.client_id,
            client_secret=config.client_secret,
        )
        yield client
        client._token_storage.clear_cache()
