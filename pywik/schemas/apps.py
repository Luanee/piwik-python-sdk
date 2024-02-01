from typing import Annotated, Literal, Type

from pydantic import AfterValidator, AliasPath, BaseModel, Field

from pywik.schemas.base import BaseSchema, Page


AppType = Literal["web"] | Literal["sharepoint"] | Literal["demo"]
GDPR = Literal["no_device_storage"] | Literal["session_cookie_id"]


class BaseApp(BaseSchema):
    name: str = Field(validation_alias=AliasPath("attributes", "name"))

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"BaseApp(id={self.id}, name='{self.name}')"


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
    gdprDataAnonymizationMode: GDPR = Field(default="session_cookie_id")
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


class AppsPage(Page[BaseApp]):
    model: Type[BaseModel] = BaseApp
