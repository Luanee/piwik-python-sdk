import warnings

from typing import Optional

from pywik.base import BaseClient
from pywik.schemas.apps import AppsPage
from pywik.schemas.base import Page


class AppsService:
    _client: BaseClient
    _endpoint: str = "/api/apps/v2"

    def __init__(self, client: BaseClient):
        self._client = client

    def list(self, search: Optional[str] = None, sort: str = "-addedAt", page: int = 0, size: int = 10) -> AppsPage:
        params = {
            "search": search,
            "sort": sort,
            "limit": size,
            "offset": page * size,
        }

        response = self._client._get(self._endpoint, params=params)
        if response.status_code == 200:
            return AppsPage(**response.json() | {"page": page, "size": size})
        elif response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())
            # obj = ErrorResponse.deserialize(response.json())
            # raise self._client._create_exception(obj, response)
        elif response.status_code != 404:
            warnings.warn("Unhandled status code %d" % response.status_code)
        else:
            pass

        return AppsPage(**response.json() | {"page": page, "size": size})

    def get(self):
        return

    def create(self):
        return

    def delete(self):
        return

    def update(self):
        return
