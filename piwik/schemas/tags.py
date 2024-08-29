from typing import Annotated, Literal, Optional, get_args

from pydantic import AfterValidator, Field, computed_field, field_validator

from piwik.schemas.base import BaseSchema, DateMixin
from piwik.schemas.mixins import PaginationMixin
from piwik.schemas.types import PathChoices
from piwik.schemas.utils import validate_comma_separated_string

TagType = Literal["tag"]
TAG_TYPE: TagType = get_args(TagType)[0]


CONSENT_TYPE = (
    Literal["not_require_consent"]
    | Literal["analytics"]
    | Literal["ab_testing_and_personalization"]
    | Literal["conversion_tracking"]
    | Literal["marketing_automation"]
    | Literal["remarketing"]
    | Literal["user_feedback"]
    | Literal["custom_consent"]
)

SORT = (
    Literal["name"]
    | Literal["is_active"]
    | Literal["tag_type"]
    | Literal["priority"]
    | Literal["created_at"]
    | Literal["updated_at"]
)

TEMPLATE = (
    Literal["adroll"]
    | Literal["bing_ads"]
    | Literal["crazy_egg"]
    | Literal["custom_content"]
    | Literal["custom_popup"]
    | Literal["custom_tag"]
    | Literal["doubleclick_floodlight"]
    | Literal["facebook_retargeting_pixel"]
    | Literal["google_analytics"]
    | Literal["hot_jar"]
    | Literal["hub_spot"]
    | Literal["linkedin"]
    | Literal["marketo"]
    | Literal["mautic"]
    | Literal["piwik"]
    | Literal["piwik_custom_dimension"]
    | Literal["piwik_event"]
    | Literal["piwik_goal_conversion"]
    | Literal["piwik_virtual_page_view"]
    | Literal["qualaroo"]
    | Literal["sales_manago"]
    | Literal["salesforce_pardot"]
    | Literal["video_html5"]
    | Literal["video_youtube"]
    | Literal["heatmaps"]
    | Literal["abandoned"]
    | Literal["ecommerce_order"]
    | Literal["ecommerce_add_to_cart"]
    | Literal["ecommerce_remove_from_cart"]
    | Literal["ecommerce_product_detail_view"]
    | Literal["ecommerce_cart_update"]
    | Literal["cookie_information_cmp_integration"]
    | Literal["ab_tasty"]
    | Literal["click_tale"]
    | Literal["google_adwords"]
    | Literal["optimizely"]
    | Literal["visual_website_optimizer"]
)


def validate_sort(field_name: str):
    return field_validator("sort")(lambda v: validate_comma_separated_string("sort", SORT, v))


SORTING = Annotated[str, AfterValidator(validate_sort)]


class TagListRequestParameters(PaginationMixin):
    page: int = Field(default=0)
    size: int = Field(default=100, gt=0, le=500)
    name: Optional[str] = Field(default=None, serialization_alias="filter[name]")
    is_active: Optional[bool] = Field(default=None, serialization_alias="filter[is_active]")
    template: Optional[TEMPLATE] = Field(default=None, serialization_alias="filter[template]")
    is_prioritized: Optional[bool] = Field(default=None, serialization_alias="filter[is_prioritized]")
    sort: Optional[SORTING] = None

    @computed_field(alias="page[limit]", repr=False)
    @property
    def limit(self) -> int:
        return self.size

    @computed_field(alias="page[offset]", repr=False)
    @property
    def offset(self) -> int:
        return self.page * self.size

    def serialize(self):
        return self.model_dump(
            exclude={"page", "size"},
            exclude_none=True,
            by_alias=True,
        )


class Tag(BaseSchema, DateMixin):
    __repr_fields__: set[str] = {"id", "name", "priority"}

    type: TagType = Field(default=TAG_TYPE)

    is_active: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.is_active"),
    )

    is_published: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.is_published"),
    )

    priority: int = Field(
        default=0,
        ge=0,
        lt=4294967295,
        validation_alias=PathChoices("data.attributes.priority"),
    )

    name: str = Field(
        validation_alias=PathChoices("data.attributes.name"),
    )

    consent_type: CONSENT_TYPE = Field(
        validation_alias=PathChoices("data.attributes.consent_type"),
    )

    template: TEMPLATE = Field(
        validation_alias=PathChoices("data.attributes.template"),
    )
