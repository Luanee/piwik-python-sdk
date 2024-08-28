import datetime

from typing import Any, Optional, Sequence



from piwik.base import BaseService
from piwik.schemas.raw import RawAnalyticsParameter
from piwik.schemas.types import Column, RELATIVE_DATE, FORMAT, COLUMN_FORMAT
from piwik.utils.validators import validate_response


class SessionsService(BaseService):
    _endpoint: str = "/api/analytics/v1/sessions"

    def get(
        self,
        id: str,
        columns: Sequence[str | Column | dict],
        page: int = 0,
        size: int = 100,
        date_from: Optional[str | datetime.date] = None,
        date_to: Optional[str | datetime.date] = None,
        relative_date: Optional[RELATIVE_DATE] = None,
        format: Optional[FORMAT] = None,
        column_format: Optional[COLUMN_FORMAT] = None,
        compression: bool = False,
    ) -> dict[str, Any] | None:
        query = RawAnalyticsParameter(
            website_id=id,
            columns=columns,
            page=page,
            size=size,
            date_from=date_from,
            date_to=date_to,
            relative_date=relative_date,
            format=format,
            column_format=column_format,
        )

        headers = {"Accept-Encoding": "gzip"} if compression else {}

        response = self._client._post(
            f"{self._endpoint}/",
            json=query.as_body(),
            headers=headers,
        )

        validate_response(response)
        return response.json()
