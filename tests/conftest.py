import os

from unittest import mock

import pytest


@pytest.fixture
def active_piwik_environment():
    environ = {
        "PIWIK_URL": "https://<account>.piwik.pro",
        "PIWIK_AUTH_URL": "https://<account>.piwik.pro/auth/token",
        "PIWIK_CLIENT_ID": "client_id",
        "PIWIK_CLIENT_SECRET": "client_secret",
    }

    yield environ


@pytest.fixture
def inactive_piwik_environment():
    names_to_remove = {"PIWIK_URL", "PIWIK_AUTH_URL", "PIWIK_CLIENT_ID", "PIWIK_CLIENT_SECRET"}
    environ = {k: v for k, v in os.environ.items() if k not in names_to_remove}

    yield environ
