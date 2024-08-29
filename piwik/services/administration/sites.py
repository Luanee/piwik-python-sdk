import warnings
from typing import List, Literal, Optional

from piwik.base.base_client import BaseClient
from piwik.exceptions import ExceptionResponse
from piwik.schemas.page import Page
from piwik.schemas.sites import (
    BaseSite,
    MetaSiteApp,
    Site,
    SiteContainer,
    SiteCreateDraft,
    SiteIntegrity,
    SiteUpdateDraft,
)

from .apps import SEARCH


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
    ) -> Page[BaseSite]:
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
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        if response.status_code != 404:
            warnings.warn(f"Unhandled status code: {response.status_code}")

        return Page[BaseSite].deserialize(page=page, size=size)

    def get(self, id: str) -> Site | None:
        response = self._client._get(f"{self._endpoint}/{id}")

        if response.status_code == 200:
            return Site.deserialize(response.json())

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn("Unhandled status code %d" % response.status_code)

    def create(self, draft: SiteCreateDraft):
        response = self._client._post(
            f"{self._endpoint}",
            json=draft.serialize(),
        )
        if response.status_code == 201:
            return Site.deserialize(response.json())

        if response.status_code in (400, 401, 403, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn("Unhandled status code %d" % response.status_code)

    def delete(self, id: str):
        response = self._client._delete(
            f"{self._endpoint}/{id}",
        )

        if response.status_code == 204:
            return None

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn("Unhandled status code %d" % response.status_code)

    def update(self, draft: SiteUpdateDraft):
        response = self._client._patch(
            f"{self._endpoint}/{draft.id}",
            json=draft.serialize(),
        )

        if response.status_code == 204:
            return None

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn("Unhandled status code %d" % response.status_code)

    def list_apps(
        self,
        id: str,
        search: Optional[str] = None,
        sort: SEARCH = "name",
        page: int = 0,
        size: int = 10,
        type: Literal["included"] | Literal["excluded"] = "included",
    ) -> Page[MetaSiteApp]:
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
            return Page[MetaSiteApp].deserialize(response.json(), page=page, size=size)

        if response.status_code in (400, 401, 403, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        if response.status_code != 404:
            warnings.warn(f"Unhandled status code: {response.status_code}")

        return Page[MetaSiteApp].deserialize(page=page, size=size)

    def list_all_sites(
        self,
        search: Optional[str] = None,
        sort: SEARCH = "name",
        page: int = 0,
        size: int = 10,
        action: Literal["view"] | Literal["edit"] = "view",
    ) -> Page[MetaSiteApp]:
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
            return Page[MetaSiteApp].deserialize(response.json(), page=page, size=size)

        if response.status_code in (400, 401, 403, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        if response.status_code != 404:
            warnings.warn(f"Unhandled status code: {response.status_code}")

        return Page[MetaSiteApp].deserialize(page=page, size=size)

    def add_apps(self, meta_site_id: str, ids: List[str]):
        response = self._client._post(
            f"{self._endpoint}/{meta_site_id}/relationships/apps",
            json=SiteContainer(ids=ids).serialize(),
        )

        if response.status_code == 204:
            return None

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn("Unhandled status code %d" % response.status_code)

    def delete_apps(self, meta_site_id: str, ids: List[str]):
        response = self._client._delete(
            f"{self._endpoint}/{meta_site_id}/relationships/apps",
            json=SiteContainer(ids=ids).serialize(),
        )

        if response.status_code == 204:
            return None

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn("Unhandled status code %d" % response.status_code)

    def validate(self, id: str):
        response = self._client._get(f"{self._endpoint}/{id}/apps/integrity")

        if response.status_code == 200:
            return SiteIntegrity.deserialize(response.json())

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn("Unhandled status code %d" % response.status_code)
