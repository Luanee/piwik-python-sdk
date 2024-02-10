import pytest

from piwik.client import Client


@pytest.fixture()
def environment(monkeypatch):
    monkeypatch.setenv("PIWIK_CLIENT_ID", "client_id")
    monkeypatch.setenv("PIWIK_CLIENT_SECRET", "client_secret")
    monkeypatch.setenv("PIWIK_URL", "https://<account>.piwik.pro")
    monkeypatch.setenv("PIWIK_AUTH_URL", "https://<account>.piwik.pro/auth/token")
