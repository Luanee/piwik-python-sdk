import datetime
from typing import Literal, Optional, get_args

from pydantic import Field

from piwik.schemas.base import BaseSchema, CreateRequestDataMixin, UpdateRequestDataMixin
from piwik.schemas.types import PathChoices

ProductCustomDimensionType = Literal["ProductCustomDimension"]
PRODUCT_CUSTOM_DIMENSION_TYPE: ProductCustomDimensionType = get_args(ProductCustomDimensionType)[0]


class BaseProductCustomDimension(BaseSchema):
    type: ProductCustomDimensionType = Field(default=PRODUCT_CUSTOM_DIMENSION_TYPE)

    website_id: str = Field(
        validation_alias=PathChoices("data.attributes.website_id"),
    )
    name: str = Field(
        validation_alias=PathChoices("data.attributes.name"),
    )
    slot: int = Field(
        ge=1,
        validation_alias=PathChoices("data.attributes.slot"),
    )


class ProductCustomDimension(BaseProductCustomDimension):
    created_at: Optional[datetime.datetime | str] = Field(
        default=None,
        validation_alias=PathChoices("data.attributes.created_at"),
        serialization_alias="created_at",
    )
    updated_at: Optional[datetime.datetime | str] = Field(
        default=None,
        validation_alias=PathChoices("data.attributes.updatedAt"),
        serialization_alias="updatedAt",
    )


class ProductCustomDimensionCreateDraft(CreateRequestDataMixin, BaseProductCustomDimension):
    id: None = None


class ProductCustomDimensionUpdateDraft(UpdateRequestDataMixin, BaseProductCustomDimension):
    id: str
    type: ProductCustomDimensionType = Field(default=PRODUCT_CUSTOM_DIMENSION_TYPE)
    website_id: str
    name: str
    slot: int = Field(ge=1)
