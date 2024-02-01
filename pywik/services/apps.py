import warnings

from typing import Literal, Optional

from pywik.base import BaseClient
from pywik.schemas.apps import AppsPage


SEARCH = (
    Literal["name"]
    | Literal["addedAt"]
    | Literal["updatedAt"]
    | Literal["-name"]
    | Literal["-addedAt"]
    | Literal["-updatedAt"]
)

PERMISSIONS = Literal["view"] | Literal["edit"] | Literal["publish"] | Literal["manage"]


class AppsService:
    _client: BaseClient
    _endpoint: str = "/api/apps/v2"

    def __init__(self, client: BaseClient):
        self._client = client

    def list(
        self,
        search: Optional[str] = None,
        sort: SEARCH = "-addedAt",
        page: int = 0,
        size: int = 10,
        permission: Optional[PERMISSIONS] = None,
    ) -> AppsPage:
        """Get list of apps

        Args:
            search (Optional[str], optional): App search query. Defaults to None.
            sort (str, optional): Sort field - can be reversed by adding dash before field name e.g (-name). Defaults to "-addedAt".
            page (int, optional): Sets offset for list of items. Defaults to 0.
            size (int, optional): Limits the number of returned items. Defaults to 10.

        Raises:
            ValueError: _description_

        Returns:
            AppsPage: _description_
        """

        params = {
            "search": search,
            "sort": sort,
            "limit": size,
            "offset": page * size,
            "permission": permission,
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
