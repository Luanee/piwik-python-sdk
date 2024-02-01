from typing import Optional
import warnings
from pywik.base import BaseClient


class AppsService:
    _client: BaseClient
    _endpoint: str = "/api/apps/v2/"

    def __init__(self, client: BaseClient):
        self._client = client

    def list(self, search: Optional[str] = None, sort: str = "-addedAt", page: int = 0, size: int = 10):
        params = {
            "search": search,
            "sort": sort,
            "limit": size,
            "offset": page,
        }

        response = self._client._get(self._endpoint, params=params)
        # if response.status_code == 200:
        #     return Page.deserialize(response.json())
        # elif response.status_code in (400, 401, 403, 500, 502, 503):
        #     obj = ErrorResponse.deserialize(response.json())
        #     raise self._client._create_exception(obj, response)
        if response.status_code == 404:
            return None
        warnings.warn("Unhandled status code %d" % response.status_code)

    def get(self):
        return

    def create(self):
        return

    def delete(self):
        return

    def update(self):
        return
