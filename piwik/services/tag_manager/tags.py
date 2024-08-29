import warnings
from typing import Optional

from piwik.base.service import BaseService
from piwik.exceptions import ExceptionResponse
from piwik.schemas.page import Page
from piwik.schemas.tags import TEMPLATE, Tag, TagListRequestParameters


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
    ) -> Page[Tag]:
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
            return Page[Tag].deserialize(response.json(), page=page, size=size)

        if response.status_code in (400, 401, 403, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        if response.status_code != 404:
            warnings.warn(f"Unhandled status code: {response.status_code}")

        return Page[Tag].deserialize(page=page, size=size)
