import warnings

from typing import Literal, Optional

from piwik.base.base_client import BaseClient
from piwik.schemas.page import Page
from piwik.schemas.sites import BaseSite, Site, SiteIntegrity
from piwik.services.apps import SEARCH


class SitesService:
    _client: BaseClient
    _endpoint: str = "/api/meta-sites/v1"

    def __init__(self, client: BaseClient):
        self._client = client

    def list(
        self,
        search: Optional[str] = None,
        sort: SEARCH = "name",
        page: int = 0,
        size: int = 10,
    ):
        params = {
            "search": search,
            "sort": sort,
            "limit": size,
            "offset": page * size,
        }

        response = self._client._get(
            self._endpoint,
            params=params,
        )

        if response.status_code == 200:
            return Page[BaseSite].deserialize(response.json(), page=page, size=size)
        if response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(f"{str(response.json())}")
            # obj = ErrorResponse.deserialize(response.json())
            # raise self._client._create_exception(obj, response)
        if response.status_code != 404:
            warnings.warn(f"Unhandled status code: {response.status_code}")

        return Page[BaseSite].deserialize(page=page, size=size)

    def get(self, id: str) -> Site | None:
        response = self._client._get(
            f"{self._endpoint}/{id}",
        )

        if response.status_code == 200:
            return Site.deserialize(response.json())
        elif response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())
        elif response.status_code == 404:
            raise ValueError(f"Site with id: {id} could not be found.")
        else:
            warnings.warn(f"Unhandled status code: {response.status_code}")

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def list_apps(
        self,
        id: str,
        search: Optional[str] = None,
        sort: SEARCH = "name",
        page: int = 0,
        size: int = 10,
        type: Literal["included"] | Literal["excluded"] = "included",
    ):
        params = {
            "search": search,
            "sort": sort,
            "limit": size,
            "offset": page * size,
        }

        response = self._client._get(
            f"{self._endpoint}/{id}/apps{'/excluded' if type == 'excluded' else ''}",
            params=params,
        )

        if response.status_code == 200:
            return Page[BaseSite].deserialize(response.json(), page=page, size=size)
        if response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(f"{str(response.json())}")
            # obj = ErrorResponse.deserialize(response.json())
            # raise self._client._create_exception(obj, response)
        if response.status_code != 404:
            warnings.warn(f"Unhandled status code: {response.status_code}")

    def list_all_sites(
        self,
        search: Optional[str] = None,
        sort: SEARCH = "name",
        page: int = 0,
        size: int = 10,
        action: Literal["view"] | Literal["edit"] = "view",
    ):
        params = {
            "search": search,
            "sort": sort,
            "limit": size,
            "offset": page * size,
            "action": action,
        }

        response = self._client._get(
            f"{self._endpoint}/apps-with-meta-sites",
            params=params,
        )

        if response.status_code == 200:
            return Page[BaseSite].deserialize(response.json(), page=page, size=size)
        if response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(f"{str(response.json())}")
            # obj = ErrorResponse.deserialize(response.json())
            # raise self._client._create_exception(obj, response)
        if response.status_code != 404:
            warnings.warn(f"Unhandled status code: {response.status_code}")

    def add_apps(self):
        pass

    def delete_apps(self):
        pass

    def validate(self, id: str):
        response = self._client._get(f"{self._endpoint}/{id}/apps/integrity")

        if response.status_code == 200:
            return SiteIntegrity.deserialize(response.json())
        elif response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())
        elif response.status_code == 404:
            raise ValueError(f"Site with id: {id} could not be found.")
        else:
            warnings.warn(f"Unhandled status code: {response.status_code}")
