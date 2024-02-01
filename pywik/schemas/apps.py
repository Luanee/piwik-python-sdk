from enum import Enum
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, Field
from pywik.schemas.base import BaseSchema


AppType = Literal["web"] | Literal["sharepoint"] | Literal["demo"]


class BaseApp(BaseSchema):
    name: str


class App(BaseApp):
    organization: str
    app_type: AppType
    urls: list[str]
    timezone: str
    currency: str
    excludeUnknownUrls: bool = Field(default=False)
    keepUrlFragment: bool = Field(default=True)
    eCommerceTracking: bool = Field(default=True)
    siteSearchQueryParams: list[str] = Field(default=["q", "query", "s", "search", "searchword", "keyword"])
    siteSearchCategoryParams: list = Field(default_factory=list)
    delay: int = Field(default=500)
    excludedIps: list[str] = Field(default_factory=list)
    excludedUrlParams: list[str] = Field(default_factory=list)
    excludedUserAgents: list[str] = Field(default_factory=list)
    gdpr: bool = Field(default=True)
    gdprUserModeEnabled: bool = Field(default=False)
    privacyCookieDomainsEnabled: bool = Field(default=False)
    privacyCookieExpirationPeriod: int = Field(default=31536000)
    privacyCookieDomains: list[str] = Field(default_factory=list)
    gdprLocationRecognition: bool = Field(default=True)
    gdprDataAnonymization: bool = Field(default=True)
    sharepointIntegration: bool = Field(default=False)
    gdprDataAnonymizationMode: Literal["no_device_storage"] | Literal["session_cookie_id"] = Field(
        default="session_cookie_id"
    )
    privacyUseCookies: bool = Field(default=True)
    privacyUseFingerprinting: bool = Field(default=True)
    cnil: bool = Field(default=False)
    sessionIdStrictPrivacyMode: bool = Field(default=False)


def urls_startswith(urls: list[str]):
    if all(url.startswith("http://") or url.startswith("https://") for url in urls):
        return urls
    raise ValueError("URLs should start with one of: 'http://' or 'https://'.")


URLS = Annotated[list[str], AfterValidator(urls_startswith)]


class AppDraft(BaseModel):
    name: str = Field(default=..., max_length=90)
    urls: URLS
