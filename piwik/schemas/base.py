import datetime

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from piwik.schemas.utils import PathChoices


class DeserializeMixin(BaseModel):

    @classmethod
    def deserialize(cls, data: dict[str, Any]):
        return cls(**data)


class SerializeMixin(BaseModel):

    def serialize(self) -> dict[str, Any]:
        return self.model_dump()


class ReprMixin(BaseModel):
    __repr_fields__: set[str] = {"id"}

    def __repr__(self):
        fields = self.model_dump(include=self.__repr_fields__)
        description = ",".join(
            [f"{key}='{value}'" for key, value in fields.items() if not (key == "id" and value is None)]
        )
        return f"{self.__class__.__name__}({description})"


class BaseSchema(DeserializeMixin, SerializeMixin, ReprMixin):
    # __repr_fields__: set[str] = {"id"}

    type: str = Field(
        validation_alias=PathChoices("data.type"),
        frozen=True,
    )
    id: str = Field(
        validation_alias=PathChoices("data.id"),
        frozen=True,
    )
    addedAt: datetime.datetime = Field(
        default=None,
        validation_alias=PathChoices("data.attributes.addedAt"),
    )
    updatedAt: Optional[datetime.datetime] = Field(
        default=None,
        validation_alias=PathChoices("data.attributes.updatedAt"),
    )

    model_config = ConfigDict(populate_by_name=True)

    # @classmethod
    # def deserialize(cls, data: dict[str, Any]):
    #     return cls(**data)

    # def serialize(self) -> dict[str, Any]:
    #     return self.model_dump()

    def __str__(self):
        return repr(self)

    # def __repr__(self):
    #     fields = self.model_dump(include=self.__repr_fields__)
    #     description = ",".join(
    #         [f"{key}='{value}'" for key, value in fields.items() if not (key == "id" and value is None)]
    #     )
    #     return f"{self.__class__.__name__}({description})"


class BaseSite(BaseSchema):
    __repr_fields__: set[str] = {"id", "name"}

    name: str = Field(default=..., max_length=90, validation_alias=PathChoices("data.attributes.name"))


class RequestDataMixin(BaseModel):
    def serialize(self, exclude: Optional[set] = None) -> dict[str, Any]:
        data = self.model_dump(include=exclude)
        attributes = self.model_dump(exclude=exclude, exclude_unset=True)
        return {
            "data": {
                **data,
                "attributes": attributes,
            }
        }


class UpdateRequestDataMixin(RequestDataMixin):
    def serialize(self):
        return RequestDataMixin.serialize(self, exclude={"id", "type"})


class CreateRequestDataMixin(RequestDataMixin):

    def serialize(self):
        return RequestDataMixin.serialize(self, exclude={"type"})
