from pydantic import BaseModel, Field

from piwik.schemas.base import PathChoices, RequestDataMixin


class BaseSite(BaseModel):
    pass


class Site(BaseModel):
    pass


class SiteUpdateDraft(RequestDataMixin):
    pass


class SiteCreateDraft(RequestDataMixin):
    pass


class SiteIntegrity(BaseModel):
    is_currency_valid: bool = Field(validation_alias=PathChoices("data.attributes.valid_currency"))
    is_timezone_valid: bool = Field(validation_alias=PathChoices("data.attributes.valid_timezone"))
