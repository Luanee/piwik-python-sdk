import datetime
from typing import Any, Optional, Sequence

from piwik.base import BaseService
from piwik.schemas.raw import QueryAnalyticsParameter
from piwik.schemas.types import COLUMN_FORMAT, FORMAT, RELATIVE_DATE, Column
from piwik.utils.validators import validate_response


class QueriesService(BaseService):
    _endpoint: str = "/api/analytics/v1/query/"

    def execute(
        self,
        id: str,
        columns: Sequence[str | Column | dict],
        page: int = 0,
        size: int = 100,
        date_from: Optional[str | datetime.date] = None,
        date_to: Optional[str | datetime.date] = None,
        relative_date: Optional[RELATIVE_DATE] = None,
        format: Optional[FORMAT] = "json",
        column_format: Optional[COLUMN_FORMAT] = "id",
        sampling: Optional[float] = None,
        compression: bool = False,
    ) -> dict[str, Any] | None:
        query = QueryAnalyticsParameter(
            website_id=id,
            columns=columns,
            page=page,
            size=size,
            date_from=date_from,
            date_to=date_to,
            relative_date=relative_date,
            format=format,
            column_format=column_format,
            sampling=sampling,
        )

        headers = {"Accept-Encoding": "gzip"} if compression else {}

        response = self._client._post(
            f"{self._endpoint}/",
            json=query.serialize(),
            headers=headers,
        )

        validate_response(response)
        return response.json()
