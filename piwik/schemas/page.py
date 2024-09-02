from typing import Any, Generic, Optional, TypeVar

from pydantic import AliasPath, AnyUrl, BaseModel, Field

from piwik.schemas.base import BaseSchema

TSchema = TypeVar("TSchema", bound=BaseSchema)


class Links(BaseModel):
    self: AnyUrl = Field(..., description="Link to current page")
    first: Optional[AnyUrl] = Field(default=None, description="Link to first page")
    last: Optional[AnyUrl] = Field(default=None, description="Link to last page")
    prev: Optional[AnyUrl] = Field(default=None, description="Link to previous page")
    next: Optional[AnyUrl] = Field(default=None, description="Link to next page")


class Page(BaseModel, Generic[TSchema]):
    page: int = Field(default=0)
    size: int = Field(default=10)
    total: int = Field(validation_alias=AliasPath("meta", "total"), default=0)
    data: list[TSchema] = Field(validation_alias=AliasPath("data"), default_factory=list)
    links: Links = Field(..., description="Pagination links")

    @classmethod
    def deserialize(cls, data: Optional[dict[str, Any]] = None, page: int = 0, size: int = 10):
        data = data or {}
        return cls(**data, page=page, size=size)

    def serialize(self) -> dict[str, Any]:
        return self.model_dump()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        type_name = "Unknown"

        if self.data and isinstance(self.data[0], BaseModel):
            type_name = self.data[0].__class__.__name__
        elif hasattr(self, "__pydantic_generic_metadata__"):
            for base in self.__pydantic_generic_metadata__.get("args", []):
                type_name = base.__name__
                break

        return f"Page<{type_name}>(page={self.page}, size={self.size}, total={self.total})"

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, index: int):
        return self.data[index]
