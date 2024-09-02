from typing import Annotated, Literal, Optional, get_args

from pydantic import AfterValidator, BaseModel, Field, computed_field, field_validator

from piwik.schemas.base import BaseSchema, CreateRequestDataMixin, DateMixin, RequestDataMixin, UpdateRequestDataMixin
from piwik.schemas.mixins import PaginationMixin
from piwik.schemas.triggers import TriggerReference
from piwik.schemas.types import PathChoices
from piwik.schemas.utils import DateTimeString, TimeString, validate_comma_separated_string

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


class Relationships(BaseModel):
    triggers: list[TriggerReference] = Field(
        ...,
        min_length=1,
        validation_alias=PathChoices("triggers.data"),
        description="Trigger relationship",
    )


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


class _BaseTag(BaseSchema):
    pass


class BaseTag(_BaseTag, DateMixin):
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
        description="Order of firing tags (bigger number means earlier)",
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
    relationships: Optional[Relationships] = Field(
        default=None,
        validation_alias=PathChoices("data.relationships"),
        description="Relationships with triggers",
    )


class Tag(BaseTag):
    code: str = Field(
        ...,
        min_length=1,
        max_length=65536,
        description="Tag code (html, script or css)",
        validation_alias=PathChoices("data.attributes.code"),
    )


class TagCreateDraft(CreateRequestDataMixin, Tag):
    id: None = None

    def serialize(self):
        has_relationships = "relationships" in self.model_fields
        data = RequestDataMixin.serialize(
            self, data_fields={"id", "type"}, exclude={"relationships"} if has_relationships else None
        )
        relationships = self.model_dump(include={"relationships"})

        return {
            **data,
            **relationships,
        }


class TagUpdateDraft(UpdateRequestDataMixin, Tag):
    pass


class TagCopy(_BaseTag):
    operation_id: str = Field(validation_alias=PathChoices("data.relationships.operations.data.id"))


class TagCopyDraft(RequestDataMixin, _BaseTag):
    id: str
    name: str
    app_id: Optional[str] = Field(default=None)
    with_triggers: bool = Field(default=False)

    def set_app_id(self, app_id: str):
        if not self.app_id or self.app_id != app_id:
            self.app_id = app_id
        return self

    def serialize(self):
        data = RequestDataMixin.serialize(self, exclude={"id", "type"})
        return {
            **data,
            "relationships": {
                "target_app": {
                    "data": {
                        "id": self.app_id,
                        "type": "app",
                    }
                }
            },
        }


class DateDefinition(BaseModel):
    date_from: DateTimeString = Field(
        ...,
        alias="from",
        description="format: Y-m-d\\TH:i:sO (https://www.php.net/manual/en/class.datetimeinterface.php#datetime.constants.iso8601)",
        title="Date",
        serialization_alias="from_",
    )
    date_to: DateTimeString = Field(
        ...,
        description="format: Y-m-d\\TH:i:sO (https://www.php.net/manual/en/class.datetimeinterface.php#datetime.constants.iso8601)",
        title="Date",
        serialization_alias="to",
    )
    timezone: str = Field(
        ...,
        description="Time zone definition (https://www.php.net/manual/en/timezones.php#timezones)",
        title="Timezone",
    )


class TimeDefinition(BaseModel):
    date_from: TimeString = Field(
        ...,
        alias="from",
        description="format: H:i:s (https://www.php.net/manual/en/function.date.php#refsect1-function.date-parameters)",
        title="Time",
        serialization_alias="from_",
    )
    date_to: TimeString = Field(
        ...,
        description="format: H:i:s (https://www.php.net/manual/en/function.date.php#refsect1-function.date-parameters)",
        title="Time",
        serialization_alias="to",
    )
    timezone: str = Field(
        ...,
        description="Time zone definition (https://www.php.net/manual/en/timezones.php#timezones)",
        title="Timezone",
    )


class Scheduler(BaseModel):
    date_ranges: list[DateDefinition] = Field(..., min_length=1, description="Tag flight date definition")
    times_of_day: list[TimeDefinition] = Field(..., min_length=1, description="Tag flight time definition")
