import datetime

from typing import Any, Generic, Type, TypeVar

from pydantic import AliasChoices, AliasPath, BaseModel, ConfigDict, Field


class PathChoices(AliasChoices):
    def __init__(self, field: str) -> None:
        fields = field.split(".")
        paths = [AliasPath(*fields[index:]) for index, _ in enumerate(reversed(fields))]
        super().__init__(*paths)


class BaseSchema(BaseModel):
    type: str = Field(
        validation_alias=PathChoices("data.type"),
        frozen=True,
    )
    id: str = Field(
        validation_alias=PathChoices("data.id"),
    )
    addedAt: datetime.datetime = Field(
        default=None,
        validation_alias=PathChoices("data.attributes.addedAt"),
    )
    updatedAt: datetime.datetime = Field(
        default=None,
        validation_alias=PathChoices("data.attributes.updatedAt"),
    )

    model_config = ConfigDict(populate_by_name=True)

    @classmethod
    def deserialize(cls, data: dict[str, Any]):
        return cls(**data)

    def serialize(self) -> dict[str, Any]:
        return self.model_dump()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"{self.__name__}(id={self.id})"


TSchema = TypeVar("TSchema", bound=BaseModel)


class Page(BaseModel, Generic[TSchema]):
    model: Type[BaseModel] = Field(exclude=True)

    page: int = Field(default=0)
    size: int = Field(default=10)
    total: int = Field(validation_alias=AliasPath("meta", "total"))
    data: list[TSchema] = Field(validation_alias=AliasPath("data"))

    @classmethod
    def deserialize(cls, data: dict[str, Any], page: int, size: int):
        return cls(**data, page=page, size=size)

    def serialize(self) -> dict[str, Any]:
        return self.model_dump()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"Page<{self.model.__name__}>(page={self.page}, size={self.size}, total={self.total})"

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, item):
        return self.data[item]
