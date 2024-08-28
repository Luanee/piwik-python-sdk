from typing import Optional, Sequence

from pydantic import Field, field_validator, model_validator

from piwik.schemas.mixins import DateRangeMixin, PaginationMixin, RelativeDateMixin
from piwik.schemas.types import COLUMN_FORMAT, FORMAT, Column, FilterCondition


class RawAnalyticsParameter(PaginationMixin, DateRangeMixin, RelativeDateMixin):
    website_id: str
    columns: Sequence[str | Column | dict]
    format: Optional[FORMAT] = Field(default="json-kv")
    column_format: Optional[COLUMN_FORMAT] = Field(default="id")
    size: int = Field(default=500, gt=0, le=10000)
    filters: Optional[list[FilterCondition]] = Field(default=None)

    @field_validator("columns")
    @classmethod
    def validate_columns(cls, columns: Sequence[str | Column | dict]) -> list[Column]:
        return [Column.create(col) for col in columns]

    @model_validator(mode="before")
    def validate_date_parameters(cls, values):
        date_from, date_to, relative_date = (
            values.get("date_from"),
            values.get("date_to"),
            values.get("relative_date"),
        )

        if not (date_from or date_to or relative_date):
            raise ValueError("Absolute or relative dates are required: 'date_from' or 'date_to' or 'relative_date'")

        if (date_from or date_to) and relative_date:
            raise ValueError("Neither 'date_from' or 'date_to' can be used with relative_date field at the same time.")

        return values

    def serialize(self):
        return self.model_dump(exclude={"page", "size"}, exclude_none=True)


class QueryAnalyticsParameter(RawAnalyticsParameter):
    sampling: Optional[float] = Field(default=None, gt=0, le=1)

    def serialize(self):
        data = self.model_dump(exclude={"page", "size", "sampling"}, exclude_none=True)
        options = self.model_dump(include={"sampling"}, exclude_none=True, exclude_unset=True)
        return {
            **data,
            "options": options,
        }
