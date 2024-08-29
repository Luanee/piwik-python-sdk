from typing import Annotated, Literal, Optional, get_args

from pydantic import AfterValidator, Field

from piwik.schemas.base import (
    BaseSchema,
    BaseSite,
    CreateRequestDataMixin,
    DateMixin,
    UpdateRequestDataMixin,
)
from piwik.schemas.types import PathChoices
from piwik.schemas.utils import urls_startswith

AppType = Literal["ppms/app"]
APP_TYPE: AppType = get_args(AppType)[0]

AppTypes = Literal["web"] | Literal["sharepoint"] | Literal["demo"]
GDPR = Literal["no_device_storage"] | Literal["session_cookie_id"]
URLS = Annotated[list[str], AfterValidator(urls_startswith)]


class App(BaseSite):
    type: AppType = Field(default=APP_TYPE)

    organization: str = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.organization"),
    )
    app_type: AppTypes = Field(
        default="web",
        validation_alias=PathChoices("data.attributes.appType"),
    )
    urls: URLS = Field(
        validation_alias=PathChoices("data.attributes.urls"),
    )
    timezone: str = Field(
        default="UTC",
        validation_alias=PathChoices("data.attributes.timezone"),
    )
    currency: str = Field(
        default="USD",
        validation_alias=PathChoices("data.attributes.currency"),
    )
    excludeUnknownUrls: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.excludeUnknownUrls"),
    )
    keepUrlFragment: bool = Field(
        default=True,
        validation_alias=PathChoices("data.attributes.keepUrlFragment"),
    )
    eCommerceTracking: bool = Field(
        default=True,
        validation_alias=PathChoices("data.attributes.eCommerceTracking"),
    )
    siteSearchQueryParams: list[str] = Field(
        default=["q", "query", "s", "search", "searchword", "keyword"],
        validation_alias=PathChoices("data.attributes.siteSearchQueryParams"),
    )
    siteSearchCategoryParams: list = Field(
        default_factory=list,
        validation_alias=PathChoices("data.attributes.siteSearchCategoryParams"),
    )
    delay: int = Field(
        default=500,
        validation_alias=PathChoices("data.attributes.delay"),
    )
    excludedIps: list[str] = Field(
        default_factory=list,
        validation_alias=PathChoices("data.attributes.excludedIps"),
    )
    excludedUrlParams: list[str] = Field(
        default_factory=list,
        validation_alias=PathChoices("data.attributes.excludedUrlParams"),
    )
    excludedUserAgents: list[str] = Field(
        default_factory=list,
        validation_alias=PathChoices("data.attributes.excludedUserAgents"),
    )
    gdpr: bool = Field(
        default=True,
        validation_alias=PathChoices("data.attributes.gdpr"),
    )
    gdprUserModeEnabled: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.gdprUserModeEnabled"),
    )
    privacyCookieDomainsEnabled: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.privacyCookieDomainsEnabled"),
    )
    privacyCookieExpirationPeriod: int = Field(
        default=31536000,
        validation_alias=PathChoices("data.attributes.privacyCookieExpirationPeriod"),
    )
    privacyCookieDomains: list[str] = Field(
        default_factory=list,
        validation_alias=PathChoices("data.attributes.privacyCookieDomains"),
    )
    gdprLocationRecognition: bool = Field(
        default=True,
        validation_alias=PathChoices("data.attributes.gdprLocationRecognition"),
    )
    gdprDataAnonymization: bool = Field(
        default=True,
        validation_alias=PathChoices("data.attributes.gdprDataAnonymization"),
    )
    sharepointIntegration: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.sharepointIntegration"),
    )
    gdprDataAnonymizationMode: GDPR = Field(
        default="session_cookie_id",
        validation_alias=PathChoices("data.attributes.gdprDataAnonymizationMode"),
    )
    privacyUseCookies: bool = Field(
        default=True,
        validation_alias=PathChoices("data.attributes.privacyUseCookies"),
    )
    privacyUseFingerprinting: bool = Field(
        default=True,
        validation_alias=PathChoices("data.attributes.privacyUseFingerprinting"),
    )
    cnil: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.cnil"),
    )
    sessionIdStrictPrivacyMode: bool = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.sessionIdStrictPrivacyMode"),
    )


class AppUpdateDraft(UpdateRequestDataMixin, App):
    id: str
    type: AppType = Field(default=APP_TYPE)
    name: Optional[str] = Field(default=None)
    urls: Optional[URLS] = Field(default=None)


class AppCreateDraft(CreateRequestDataMixin, App):
    id: None = None


class AppPermission(BaseSchema, DateMixin):
    name: str = Field(validation_alias=PathChoices("data.attributes.app_name"))
    access: str = Field(validation_alias=PathChoices("data.attributes.access"))
