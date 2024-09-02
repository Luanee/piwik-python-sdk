import warnings
from typing import Optional

from piwik.base.service import BaseService
from piwik.exceptions import ExceptionResponse
from piwik.schemas.page import Page
from piwik.schemas.tags import (
    TEMPLATE,
    BaseTag,
    Tag,
    TagCopy,
    TagCopyDraft,
    TagCreateDraft,
    TagListRequestParameters,
    TagUpdateDraft,
)


class TagsService(BaseService):
    _endpoint: str = "/api/tag/v1/{app_id}/tags"

    def list(
        self,
        app_id: str,
        page: int = 0,
        size: int = 100,
        name: Optional[str] = None,
        is_active: Optional[bool] = None,
        template: Optional[TEMPLATE] = None,
        is_prioritized: Optional[bool] = None,
        sort: Optional[str] = None,
    ) -> Page[BaseTag]:
        query = TagListRequestParameters(
            page=page,
            size=size,
            name=name,
            is_active=is_active,
            template=template,
            is_prioritized=is_prioritized,
            sort=sort,
        )

        response = self._client._get(
            f"{self._endpoint}".format(app_id=app_id),
            params=query.serialize(),
        )

        if response.status_code == 200:
            return Page[BaseTag].deserialize(response.json(), page=page, size=size)

        if response.status_code in (400, 401, 403, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        if response.status_code != 404:
            warnings.warn(f"Unhandled status code: {response.status_code}")

        return Page[BaseTag].deserialize(page=page, size=size)

    def get(self, app_id: str, tag_id: str) -> BaseTag | None:
        response = self._client._get(
            f"{self._endpoint}/{tag_id}".format(app_id=app_id),
        )

        if response.status_code == 200:
            return BaseTag.deserialize(response.json())

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn("Unhandled status code %d" % response.status_code)

    def create(self, app_id: str, draft: TagCreateDraft):
        response = self._client._post(
            f"{self._endpoint}".format(app_id=app_id),
            json=draft.serialize(),
        )

        if response.status_code == 201:
            return Tag.deserialize(response.json())

        if response.status_code in (400, 401, 403, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn(f"Unhandled status code: {response.status_code}")

    def copy(self, app_id: str, draft: TagCopyDraft):
        draft.set_app_id(app_id)

        response = self._client._post(
            f"{self._endpoint}/{draft.id}".format(app_id=draft.app_id),
            json=draft.serialize(),
        )

        if response.status_code == 202:
            return TagCopy.deserialize(response.json())

        if response.status_code in (400, 401, 403, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn(f"Unhandled status code: {response.status_code}")

    def delete(self, app_id: str, tag_id: str):
        response = self._client._delete(
            f"{self._endpoint}/{tag_id}".format(app_id=app_id),
        )

        if response.status_code == 204:
            return None

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn(f"Unhandled status code: {response.status_code}")

    def update(self, app_id: str, draft: TagUpdateDraft):
        response = self._client._patch(
            f"{self._endpoint}/{draft.id}".format(app_id=app_id),
            json=draft.serialize(),
        )

        if response.status_code == 204:
            return None

        if response.status_code in (400, 401, 403, 404, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        warnings.warn(f"Unhandled status code: {response.status_code}")
