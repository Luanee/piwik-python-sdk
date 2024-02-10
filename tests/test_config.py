import os
import pprint

from contextlib import nullcontext as does_not_raise
from typing import Type
from unittest import mock

import pytest

from pydantic import ValidationError

from piwik.base.config import ClientConfig
from tests.conftest import active_piwik_environment, inactive_piwik_environment


@pytest.mark.parametrize(
    "config,data,environment,exception",
    [
        (
            ClientConfig,
            {
                "client_id": "client_id",
                "client_secret": "client_secret",
                "url": "https://<account>.piwik.pro",
                "auth_url": "https://<account>.piwik.pro/auth/token",
            },
            None,
            does_not_raise(),
        ),  # type: ignore
        (
            ClientConfig,
            {"_env_file": "./test.env"},
            None,
            does_not_raise(),
        ),  # type: ignore
        (
            ClientConfig,
            {"_env_file": None},
            {
                "PIWIK_URL": "https://<account>.piwik.pro",
                "PIWIK_AUTH_URL": "https://<account>.piwik.pro/auth/token",
                "PIWIK_CLIENT_ID": "client_id",
                "PIWIK_CLIENT_SECRET": "client_secret",
            },
            does_not_raise(),
        ),  # type: ignore
        (
            ClientConfig,
            {"_env_file": None},
            {},
            pytest.raises(ValidationError),
        ),  # type: ignore
    ],
)
def test_client_config(config: Type[ClientConfig], data: dict, environment, exception):
    if environment is not None:
        with mock.patch.dict(os.environ, environment, clear=True):
            with exception as es:
                c = config(**data)
    else:
        with exception as es:
            c = config(**data)
