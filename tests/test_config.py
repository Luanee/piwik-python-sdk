import os

from pathlib import Path

import pytest

from pydantic import ValidationError

from piwik.base.config import ClientConfig
from tests.conftest import environment


@environment()
def test_client_config_init():
    ClientConfig(
        client_id="client_id",
        client_secret="client_secret",  # type: ignore
        url="https://<account>.piwik.pro",
        auth_url="https://<account>.piwik.pro/auth/token",
    )


@environment()
def test_client_config_init_incorrect_auth_url():
    ClientConfig(
        client_id="client_id",
        client_secret="client_secret",  # type: ignore
        url="https://<account>.piwik.pro",
        auth_url="https://<account>.piwik.pro",
    )


@environment()
def test_client_config_init_without_auth_url():
    ClientConfig(
        client_id="client_id",
        client_secret="client_secret",  # type: ignore
        url="https://<account>.piwik.pro",
    )


@environment()
def test_client_config_env_file():
    ClientConfig(_env_file=Path(os.getcwd()) / "tests" / "test.env")  # type: ignore


@environment(
    PIWIK_URL="https://<account>.piwik.pro",
    PIWIK_AUTH_URL="https://<account>.piwik.pro/auth/token",
    PIWIK_CLIENT_ID="client_id",
    PIWIK_CLIENT_SECRET="client_secret",
)
def test_client_config_environment():
    ClientConfig()


@environment()
def test_client_config_invalid():
    with pytest.raises(ValidationError):
        ClientConfig()
