from typing import Any, Literal, Optional, get_args

from pydantic import BaseModel, Field

from piwik.schemas.apps import APP_TYPE, AppType
from piwik.schemas.base import (
    BaseSite,
    CreateRequestDataMixin,
    DeserializeMixin,
    PathChoices,
    ReprMixin,
    SerializeMixin,
    UpdateRequestDataMixin,
)


SiteType = Literal["ppms/meta-site"]
SITE_TYPE: SiteType = get_args(SiteType)[0]


class MetaSiteApp(BaseSite):
    timezone: str = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.timezone"),
    )
    currency: str = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.currency"),
    )
    cnil: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.cnil"),
    )


class Site(MetaSiteApp):
    type: SiteType = Field(
        default=SITE_TYPE,
        frozen=True,
    )
    e_commerce_tracking: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.e_commerce_tracking"),
    )
    sharepoint_integration: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.sharepoint_integration"),
    )


class SiteUpdateDraft(UpdateRequestDataMixin, Site):
    id: str
    type: SiteType = Field(default=SITE_TYPE)
    name: Optional[str] = Field(default=None)


class SiteCreateDraft(CreateRequestDataMixin, Site):
    id: None = None


class SiteContainer(BaseModel):
    type: AppType = Field(
        default=APP_TYPE,
        frozen=True,
    )
    ids: list[str]

    def serialize(self) -> dict[str, Any]:
        return {"data": [{"type": self.type, "id": id} for id in self.ids]}


class SiteIntegrity(DeserializeMixin, SerializeMixin, ReprMixin):
    __repr_fields__: set[str] = {"id", "is_currency_valid", "is_timezone_valid"}

    type: str = Field(
        validation_alias=PathChoices("data.type"),
        frozen=True,
    )
    id: str = Field(
        validation_alias=PathChoices("data.id"),
        frozen=True,
    )
    is_currency_valid: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.valid_currency"),
    )
    is_timezone_valid: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.valid_timezone"),
    )
