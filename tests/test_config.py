import os
from pathlib import Path

import pytest
from pydantic import ValidationError

from piwik.base.config import ClientConfig

ClientConfigMock = ClientConfig
ClientConfigMock.model_config["env_file"] = None


def test_client_config_init():
    ClientConfigMock(
        client_id="client_id",
        client_secret="client_secret",  # type: ignore
        url="https://<account>.piwik.pro",
        auth_url="https://<account>.piwik.pro/auth/token",
    )


def test_client_config_init_incorrect_auth_url():
    ClientConfigMock(
        client_id="client_id",
        client_secret="client_secret",  # type: ignore
        url="https://<account>.piwik.pro",
        auth_url="https://<account>.piwik.pro",
    )


def test_client_config_init_without_auth_url():
    ClientConfigMock(
        client_id="client_id",
        client_secret="client_secret",  # type: ignore
        url="https://<account>.piwik.pro",
    )


def test_client_config_env_file():
    ClientConfigMock(_env_file=Path(os.getcwd()) / "tests" / "test.env")  # type: ignore


@pytest.mark.skip
def test_client_config_invalid():
    with pytest.raises(ValidationError):
        ClientConfig()


@pytest.mark.parametrize(
    "environment",
    [
        {
            "PIWIK_URL": "https://<account>.piwik.pro",
            "PIWIK_AUTH_URL": "https://<account>.piwik.pro/auth/token",
            "PIWIK_CLIENT_ID": "client_id",
            "PIWIK_CLIENT_SECRET": "client_secret",
        },
    ],
    indirect=True,
)
def test_client_config_environment(environment):
    with environment:
        ClientConfigMock()
