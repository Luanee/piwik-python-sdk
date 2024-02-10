import warnings

from typing import Literal, Optional

from piwik.base import BaseClient
from piwik.schemas.apps import App, AppPermissionsPage, AppsPage, AppUpdateDraft


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

        response = self._client._get(
            self._endpoint,
            params=params,
        )

        if response.status_code == 200:
            return AppsPage.deserialize(response.json(), page=page, size=size)
        if response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())
            # obj = ErrorResponse.deserialize(response.json())
            # raise self._client._create_exception(obj, response)
        if response.status_code != 404:
            warnings.warn("Unhandled status code %d" % response.status_code)

        return AppsPage.deserialize({"data": []}, page=page, size=size)

    def get(self, id: str) -> App | None:
        response = self._client._get(
            f"{self._endpoint}/{id}",
        )

        if response.status_code == 200:
            return App.deserialize(response.json())
        elif response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())
        elif response.status_code == 404:
            raise ValueError(f"App with id: {id} could not be found.")
        else:
            warnings.warn("Unhandled status code %d" % response.status_code)

    def create(self, draft: AppUpdateDraft):
        response = self._client._post(
            f"{self._endpoint}",
            json=draft.serialize(),
        )
        if response.status_code == 201:
            return App.deserialize(response.json())
        if response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())

        warnings.warn("Unhandled status code %d" % response.status_code)

    def delete(self, id: str):
        response = self._client._delete(
            f"{self._endpoint}/{id}",
        )

        if response.status_code == 204:
            return None
        if response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())
        if response.status_code == 404:
            raise ValueError(f"App with id: {id} could not be found.")

        warnings.warn("Unhandled status code %d" % response.status_code)

    def update(self, draft: AppUpdateDraft):
        response = self._client._patch(
            f"{self._endpoint}/{draft.id}",
            json=draft.serialize(),
        )

        if response.status_code == 204:
            return None
        if response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())
        if response.status_code == 404:
            raise ValueError(f"App with id: {draft.id} could not be found.")

        warnings.warn("Unhandled status code %d" % response.status_code)

    def permissions(
        self,
        user_group_id: str,
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
            f"{self._endpoint}/user-group/{user_group_id}/permissions",
            params=params,
        )

        if response.status_code == 204:
            return AppPermissionsPage.deserialize(response.json(), page=page, size=size)
        if response.status_code in (400, 401, 403, 500, 502, 503):
            raise ValueError(response.json())
        if response.status_code == 404:
            raise ValueError(f"App permissions for user group id: {user_group_id} couldn't not be found.")

        warnings.warn("Unhandled status code %d" % response.status_code)
