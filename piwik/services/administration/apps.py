import warnings
from typing import Literal, Optional

from piwik.base import BaseClient
from piwik.exceptions import ExceptionResponse
from piwik.schemas.apps import App, AppCreateDraft, AppPermission, AppUpdateDraft
from piwik.schemas.base import BaseSite
from piwik.schemas.page import Page

SORT = (
    Literal["name"]
    | Literal["addedAt"]
    | Literal["updatedAt"]
    | Literal["cnil"]
    | Literal["-name"]
    | Literal["-addedAt"]
    | Literal["-updatedAt"]
    | Literal["-cnil"]
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
        sort: SORT = "-addedAt",
        page: int = 0,
        size: int = 10,
        permission: Optional[PERMISSIONS] = None,
    ) -> Page[BaseSite]:
        """Get list of apps

        Args:
            search (Optional[str], optional): App search query. Defaults to None.
            sort (str, optional): Sort field - can be reversed by adding dash before field name e.g (-name). Defaults to "-addedAt".
            page (int, optional): Sets offset for list of items. Defaults to 0.
            size (int, optional): Limits the number of returned items. Defaults to 10.

        Raises:
            ValueError: _description_

        Returns:
            Page[BaseApp]: _description_
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
            return Page[BaseSite].deserialize(response.json(), page=page, size=size)

        if response.status_code in (400, 401, 403, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        if response.status_code != 404:
            warnings.warn(f"Unhandled status code: {response.status_code}")

        return Page[BaseSite].deserialize(page=page, size=size)

    def get(self, id: str) -> App | None:
        response = self._client._get(
            f"{self._endpoint}/{id}",
        )

        if response.status_code == 200:
            return App.deserialize(response.json())

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn("Unhandled status code %d" % response.status_code)

    def create(self, draft: AppCreateDraft):
        response = self._client._post(
            f"{self._endpoint}",
            json=draft.serialize(),
        )

        if response.status_code == 201:
            return App.deserialize(response.json())

        if response.status_code in (400, 401, 403, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn(f"Unhandled status code: {response.status_code}")

    def delete(self, id: str):
        response = self._client._delete(
            f"{self._endpoint}/{id}",
        )

        if response.status_code == 204:
            return None

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn(f"Unhandled status code: {response.status_code}")

    def update(self, draft: AppUpdateDraft):
        response = self._client._patch(
            f"{self._endpoint}/{draft.id}",
            json=draft.serialize(),
        )

        if response.status_code == 204:
            return None

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn(f"Unhandled status code: {response.status_code}")

    def permissions(
        self,
        user_group_id: str,
        search: Optional[str] = None,
        sort: SORT = "name",
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

        if response.status_code == 200:
            return Page[AppPermission].deserialize(response.json(), page=page, size=size)

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn(f"Unhandled status code: {response.status_code}")
