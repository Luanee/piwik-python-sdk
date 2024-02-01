from __future__ import annotations
from typing import Any, Optional
import platform
import sys

from requests import Response
from pywik.base.config import ClientConfig
from pywik.base.http import RefreshingOAuth2Session, RetryHttpAdapter
from pywik.base.token import BaseTokenStorage, DefaultTokenStorage
from requests.adapters import HTTPAdapter
from pywik.version import __version__
from oauthlib.oauth2 import BackendApplicationClient


class BaseClient:
    def __init__(
        self,
        url: Optional[str] = None,
        auth_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token_storage: Optional[BaseTokenStorage] = None,
        http_adapter: Optional[HTTPAdapter] = None,
    ) -> None:
        self._config = ClientConfig(  # pyright: ignore
            client_id=client_id,  # pyright: ignore
            client_secret=client_secret,  # pyright: ignore
            url=url,  # pyright: ignore
            auth_url=auth_url,  # pyright: ignore
        )  # pyright: ignore

        self.__token_storage = token_storage or DefaultTokenStorage()
        http_adapter = http_adapter or RetryHttpAdapter()

        client = BackendApplicationClient(client_id=self._config.client_id)

        self._http_client = RefreshingOAuth2Session(
            client=client,
            auto_refresh_url=self._config.auth_url,
            auto_refresh_kwargs={
                "grant_type": "client_credentials",
                "client_id": self._config.client_id,
                "client_secret": self._config.client_secret,
            },
            token_updater=self.__token_storage.add_token,
        )
        self._http_client.headers.update({"User-Agent": self._user_agent})
        self._http_client.mount("http://", http_adapter)
        self._http_client.mount("https://", http_adapter)

        _token = self.__token_storage.get_token(self._config.client_id)
        if _token:
            self._http_client.token = _token
        else:
            _token = self._http_client.fetch_token(
                token_url=self._config.auth_url,
                client_id=self._config.client_id,
                client_secret=self._config.client_secret,
            )
            self.__token_storage.add_token(self._config.client_id, _token)

    @property
    def _user_agent(self):
        py_version = "%d.%d" % sys.version_info[0:2]
        arch = platform.machine()
        return f"piwik-python-sdk/{__version__} Python/{py_version} ({sys.implementation.name}; {sys.platform}; {arch})"

    def _get(
        self,
        endpoint: str,
        params: dict[str, Any],
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Retrieve a single object from piwik pro"""
        return self._http_client.get(
            f"{self._config.url}{endpoint}",
            params=params,
            headers=headers,
        )

    def _post(
        self,
        endpoint: str,
        params: dict[str, Any],
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
        params: dict[str, Any],
        data: Any = None,
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
        params: dict[str, Any],
        headers: Optional[dict[str, str]] = None,
    ) -> Response:
        """Delete an object from piwik pro"""

        return self._http_client.delete(
            f"{self._config.url}{endpoint}",
            params=params,
            headers=headers,
        )
