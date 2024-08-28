from typing import Literal, Optional, get_args

from pydantic import BaseModel, Field

from piwik.schemas.base import (
    BaseSchema,
    CreateRequestDataMixin,
    UpdateRequestDataMixin,
)
from piwik.schemas.types import PathChoices

UserAnnotationType = Literal["UserAnnotation"]
USER_ANNOTATION_TYPE: UserAnnotationType = get_args(UserAnnotationType)[0]

SystemAnnotationType = Literal["SystemAnnotation"]
SYSTEM_ANNOTATION_TYPE: SystemAnnotationType = get_args(SystemAnnotationType)[0]

VisibilityTypes = Literal["private"] | Literal["public"]


class Author(BaseModel):
    email: str = Field(
        validation_alias=PathChoices("data.attributes.author.email"),
    )


class UserAnnotation(BaseSchema):
    __repr_fields__: set[str] = {"id", "name"}

    type: UserAnnotationType = Field(default=USER_ANNOTATION_TYPE)

    website_id: str = Field(
        validation_alias=PathChoices("data.attributes.website_id"),
    )

    author: Author = Field(
        validation_alias=PathChoices("data.attributes.author"),
    )

    is_author: bool = Field(
        validation_alias=PathChoices("data.attributes.is_author"),
    )

    visibility: VisibilityTypes = Field(
        default="private",
        validation_alias=PathChoices("data.attributes.visibility"),
    )

    date: str = Field(
        validation_alias=PathChoices("data.attributes.date"),
    )

    content: str = Field(
        validation_alias=PathChoices("data.attributes.content"),
    )


class UserAnnotationUpdateDraft(UpdateRequestDataMixin, UserAnnotation):
    id: str
    type: UserAnnotationType = Field(default=USER_ANNOTATION_TYPE)

    visibility: Optional[VisibilityTypes] = Field(default="private")
    website_id: str
    date: str
    content: str


class UserAnnotationCreateDraft(CreateRequestDataMixin, UserAnnotation):
    id: None = None


class SystemAnnotation(BaseSchema):
    type: SystemAnnotationType = Field(default=SYSTEM_ANNOTATION_TYPE)

    date: str = Field(
        validation_alias=PathChoices("data.attributes.date"),
    )

    content: str = Field(
        validation_alias=PathChoices("data.attributes.content"),
    )
