import datetime

from typing import Generic, Type, TypeVar

from pydantic import AliasPath, BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    type: str = Field(validation_alias=AliasPath("type"))
    id: str = Field(validation_alias=AliasPath("id"))
    addedAt: datetime.datetime = Field(validation_alias=AliasPath("attributes", "addedAt"))
    updatedAt: datetime.datetime = Field(validation_alias=AliasPath("attributes", "updatedAt"))

    model_config = ConfigDict(populate_by_name=True)


TSchema = TypeVar("TSchema", bound=BaseModel)


class Page(BaseModel, Generic[TSchema]):
    model: Type[BaseModel] = Field(exclude=True)

    page: int = Field(validation_alias=AliasPath("page"))
    size: int = Field(validation_alias=AliasPath("size"))
    total: int = Field(validation_alias=AliasPath("meta", "total"))
    data: list[TSchema] = Field(validation_alias=AliasPath("data"))

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"Page<{self.model.__name__}>(page={self.page}, size={self.size}, total='{self.total}')"
