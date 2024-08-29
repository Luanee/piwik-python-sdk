import warnings

from piwik.base import BaseService
from piwik.exceptions import ExceptionResponse
from piwik.schemas.annotations import SystemAnnotation
from piwik.schemas.page import Page


class SystemAnnotationsService(BaseService):
    _endpoint: str = "/api/analytics/v1/manage/annotation/system/"

    def list(
        self,
        website_id: str,
        page: int = 0,
        size: int = 10,
    ):
        params = {
            "website_id": website_id,
            "limit": size,
            "offset": page * size,
        }

        response = self._client._get(
            self._endpoint,
            params=params,
        )

        if response.status_code == 200:
            return Page[SystemAnnotation].deserialize(response.json(), page=page, size=size)

        if response.status_code in (400, 401, 403, 500, 502, 503):
            error = ExceptionResponse.deserialize(response)
            raise self._client._raise_for_status(error, response)

        if response.status_code != 404:
            warnings.warn(f"Unhandled status code: {response.status_code}")

        return Page[SystemAnnotation].deserialize(page=page, size=size)
