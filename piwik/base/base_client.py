from __future__ import annotations

import platform
import sys
from typing import Any, Optional

import requests
from oauthlib.oauth2 import BackendApplicationClient
from pydantic import SecretStr
from requests import Response
from requests.adapters import HTTPAdapter

from piwik.base.config import ClientConfig
from piwik.base.http import RefreshingOAuth2Session, RetryHttpAdapter
from piwik.base.token import BaseTokenStorage, DefaultTokenStorage
from piwik.exceptions import ExceptionResponse, PiwikException
from piwik.version import __version__


class BaseClient:
    def __init__(
        self,
        url: Optional[str] = None,
        auth_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str | SecretStr] = None,
        token_storage: Optional[BaseTokenStorage] = None,
        http_adapter: Optional[HTTPAdapter] = None,
    ) -> None:
        self._config = ClientConfig(
            client_id=client_id,  # pyright: ignore
            client_secret=client_secret,  # pyright: ignore
            url=url,  # pyright: ignore
            auth_url=auth_url,  # pyright: ignore
        )

        self._token_storage = token_storage or DefaultTokenStorage()
        http_adapter = http_adapter or RetryHttpAdapter()

        client = BackendApplicationClient(client_id=self._config.client_id)

        self._http_client = RefreshingOAuth2Session(
            client=client,
            auto_refresh_url=self._config.auth_url,
            auto_refresh_kwargs={
                "grant_type": "client_credentials",
                "client_id": self._config.client_id,
                "client_secret": self._config.client_secret.get_secret_value(),
            },
            token_updater=self._token_storage.add_token,
        )

        self._http_client.headers.update(self._headers)
        self._http_client.mount("http://", http_adapter)
        self._http_client.mount("https://", http_adapter)

        _token = self._token_storage.get_token(self._config.client_id)

        if not _token:
            _token = self._http_client.fetch_token(
                token_url=self._config.auth_url,
                client_id=self._config.client_id,
                client_secret=self._config.client_secret.get_secret_value(),
            )
            self._token_storage.add_token(self._config.client_id, _token)
        self._http_client.token = _token

    @property
    def _headers(self):
        return {
            "User-Agent": self._user_agent,
            "Content-Type": "application/vnd.api+json",
        }

    @property
    def _user_agent(self):
        major, minor, micro = sys.version_info[0:3]
        arch = platform.machine()
        return f"piwik-python-sdk/{__version__} Python/{major}.{minor}.{micro} ({sys.implementation.name}; {sys.platform}; {arch})"

    def _get(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Retrieve a single object from piwik pro"""
        headers = (headers or {}).update(self._headers)
        return self._http_client.get(
            f"{self._config.url}{endpoint}",
            params=params,
            headers=headers,
        )

    def _post(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        data: Any = None,
        json: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Retrieve a single object from piwik pro"""
        return self._http_client.post(
            f"{self._config.url}{endpoint}",
            params=params,
            data=data,
            json=json,
            headers=headers,
        )

    def _patch(
        self,
        endpoint: str,
        data: Any = None,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Retrieve a single object from piwik pro"""
        return self._http_client.patch(
            f"{self._config.url}{endpoint}",
            params=params,
            data=data,
            json=json,
            headers=headers,
        )

    def _delete(
        self,
        endpoint: str,
        params: Optional[dict[str, Any]] = None,
        json: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Delete an object from piwik pro"""

        return self._http_client.delete(
            f"{self._config.url}{endpoint}",
            params=params,
            json=json,
            headers=headers,
        )

    def _raise_for_status(
        self,
        error: ExceptionResponse,
        response: requests.Response,
    ):
        if not response.content:
            response.raise_for_status()

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as exc:
            error.message = exc.args[0]

        return PiwikException.deserialize(error)
