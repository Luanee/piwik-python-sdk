import datetime
from typing import Optional, Type
from pydantic import BaseModel, Field, computed_field, field_validator


class PaginationMixin(BaseModel):
    page: int = Field(default=0)
    size: int = Field(default=100, gt=0, le=500)

    @computed_field
    @property
    def limit(self) -> int:
        return self.size

    @computed_field
    @property
    def offset(self) -> int:
        return self.page * self.size


class DateRangeMixin(BaseModel):
    __date_format__: str = "%Y-%m-%dT%H:%M:%S"

    date_from: Optional[str | datetime.date | datetime.datetime] = Field(default=None)
    date_to: Optional[str | datetime.date | datetime.datetime] = Field(default=None)

    @field_validator("date_from", "date_to")
    @classmethod
    def validate_dates(
        cls: Type["DateRangeMixin"],
        date: Optional[str | datetime.date | datetime.datetime],
    ):
        if isinstance(date, str):
            return datetime.datetime.strptime(date, cls.__date_format__)
        return date


RELATIVE_DATE_PATTERN = r"last_([1-9]\d{0,2}_days|week|month|year)|today|yesterday"


class RelativeDateMixin(BaseModel):
    relative_date: Optional[str] = Field(default=None, pattern=RELATIVE_DATE_PATTERN)
