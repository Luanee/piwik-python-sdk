from pydantic import BaseModel, Field

from piwik.schemas.base import (
    BaseSite,
    CreateRequestDataMixin,
    DeserializeMixin,
    PathChoices,
    RequestDataMixin,
    SerializeMixin,
    UpdateRequestDataMixin,
)
from piwik.schemas.utils import optional


class Site(BaseSite):
    organization: str = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.organization"),
    )
    timezone: str = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.timezone"),
    )
    currency: str = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.currency"),
    )
    e_commerce_tracking: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.e_commerce_tracking"),
    )
    sharepoint_integration: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.sharepoint_integration"),
    )
    cnil: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.cnil"),
    )


@optional(exclude={"id", "type"})
class SiteUpdateDraft(UpdateRequestDataMixin, Site):
    pass


@optional(exclude={"name", "urls", "type"})
class SiteCreateDraft(CreateRequestDataMixin, Site):
    pass


class SiteIntegrity(DeserializeMixin, SerializeMixin):
    is_currency_valid: bool = Field(validation_alias=PathChoices("data.attributes.valid_currency"))
    is_timezone_valid: bool = Field(validation_alias=PathChoices("data.attributes.valid_timezone"))
