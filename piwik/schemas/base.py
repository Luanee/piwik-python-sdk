from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from piwik.schemas.types import PathChoices
from piwik.schemas.utils import DateTimeString


class DeserializeMixin(BaseModel):
    @classmethod
    def deserialize(cls, data: dict[str, Any]):
        return cls(**data)


class SerializeMixin(BaseModel):
    def serialize(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True)


class ReprMixin(BaseModel):
    __repr_fields__: set[str] = {"id"}

    def __str__(self):
        return repr(self)

    def __repr__(self):
        def _repr_field(key: str, value: Any):
            if isinstance(value, str):
                value = f"'{value}'"
            return f"{key}={value}"

        fields = self.model_dump(include=self.__repr_fields__)
        description = ",".join(
            [_repr_field(key, value) for key, value in fields.items() if not (key == "id" and value is None)]
        )
        return f"{self.__class__.__name__}({description})"


class BaseSchema(DeserializeMixin, SerializeMixin, ReprMixin):
    type: str = Field(
        validation_alias=PathChoices("data.type"),
        frozen=True,
    )
    id: str = Field(
        validation_alias=PathChoices("data.id"),
        frozen=True,
    )

    model_config = ConfigDict(populate_by_name=True)

    @field_validator("*", mode="before")
    def validate_empty_strings(cls, value: Any):
        if value == "":
            return None
        return value


class DateMixin(BaseModel):
    created_at: Optional[DateTimeString] = Field(
        default=None,
        validation_alias=PathChoices("data.attributes.addedAt", "data.attributes.created_at"),
        serialization_alias="addedAt",
    )
    updated_at: Optional[DateTimeString] = Field(
        default=None,
        validation_alias=PathChoices("data.attributes.updatedAt", "data.attributes.updated_at"),
        serialization_alias="updatedAt",
    )


class BaseSite(BaseSchema, DateMixin):
    __repr_fields__: set[str] = {"id", "name"}

    name: str = Field(
        default=...,
        max_length=90,
        validation_alias=PathChoices("data.attributes.name"),
    )


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
