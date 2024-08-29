from typing import Literal, Optional, get_args

from pydantic import BaseModel, Field

from piwik.schemas.base import BaseSchema, RequestDataMixin
from piwik.schemas.types import PathChoices

CustomDimensionSlotsType = Literal["CustomDimensionSlots"]
CUSTOM_DIMENSION_SLOTS_TYPE: CustomDimensionSlotsType = get_args(CustomDimensionSlotsType)[0]

CustomDimensionType = Literal["CustomDimension"]
CUSTOM_DIMENSION_TYPE: CustomDimensionType = get_args(CustomDimensionType)[0]

ScopeTypes = Literal["session"] | Literal["event"]
TargetTypes = Literal["page_title_regex"] | Literal["page_url_regex"] | Literal["page_query_parameter"]


class Slots(BaseModel):
    available: int
    used: int
    left: int


class CustomDimensionSlots(BaseSchema):
    type: CustomDimensionSlotsType = Field(default=CUSTOM_DIMENSION_SLOTS_TYPE)
    event: Slots = Field(
        validation_alias=PathChoices("data.attributes.event"),
    )
    session: Slots = Field(
        validation_alias=PathChoices("data.attributes.session"),
    )
    product: Slots = Field(
        validation_alias=PathChoices("data.attributes.product"),
    )


class Extraction(BaseModel):
    target: TargetTypes
    pattern: str


class BaseCustomDimension(BaseSchema):
    type: CustomDimensionType = Field(default=CUSTOM_DIMENSION_TYPE)

    website_id: str = Field(
        validation_alias=PathChoices("data.attributes.website_id"),
    )
    name: str = Field(
        validation_alias=PathChoices("data.attributes.name"),
    )
    active: bool = Field(
        validation_alias=PathChoices("data.attributes.active"),
    )
    case_sensitive: bool = Field(
        validation_alias=PathChoices("data.attributes.case_sensitive"),
    )
    scope: ScopeTypes = Field(
        validation_alias=PathChoices("data.attributes.scope"),
    )
    slot: int = Field(
        ge=1,
        validation_alias=PathChoices("data.attributes.slot"),
    )
    extractions: list[Extraction] = Field(
        min_length=1,
        validation_alias=PathChoices("data.attributes.extractions"),
    )


class CustomDimension(BaseCustomDimension):
    tracking_id: int = Field(
        default=1,
        ge=1,
        validation_alias=PathChoices("data.attributes.tracking_id"),
    )


class CustomDimensionCreateDraft(RequestDataMixin, BaseCustomDimension):
    id: None = None


class CustomDimensionUpdateDraft(RequestDataMixin, BaseCustomDimension):
    id: str
    type: CustomDimensionType = Field(default=CUSTOM_DIMENSION_TYPE)

    website_id: str
    name: str
    active: bool
    case_sensitive: bool
    scope: ScopeTypes
    slot: Optional[int] = Field(default=None, ge=1)
    extractions: Optional[list[Extraction]] = Field(default=None)
