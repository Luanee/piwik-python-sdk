import datetime
from typing import Generic, TypeVar
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    type: str
    id: str
    addedAt: datetime.datetime
    updatedAt: datetime.datetime

    model_config = ConfigDict(populate_by_name=True)


TSchema = TypeVar("TSchema", bound=BaseModel)


class Page(BaseModel, Generic[TSchema]):
    page: int
    size: int
    total: int
    data: list[TSchema]
