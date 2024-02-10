from typing import Annotated, Any, Literal, Optional, Type

from pydantic import AfterValidator, AliasPath, BaseModel, Field
from typing_extensions import Literal

from piwik.schemas.base import BaseSchema, Page, PathChoices
from piwik.schemas.decorators import optional


def urls_startswith(urls: list[str]):
    if all(
        url.startswith(
            "http://",
        )
        or url.startswith(
            "https://",
        )
        for url in urls
    ):
        return urls
    raise ValueError(
        "URLs should start with one of: 'http://' or 'https://'.",
    )


TYPE = Literal["ppms/app"]
AppType = Literal["web"] | Literal["sharepoint"] | Literal["demo"]
GDPR = Literal["no_device_storage"] | Literal["session_cookie_id"]
URLS = Annotated[list[str], AfterValidator(urls_startswith)]


class BaseApp(BaseSchema):
    name: str = Field(validation_alias=PathChoices("data.attributes.name"))

    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"BaseApp(id={self.id}, name='{self.name}')"


# class AppsPage(Page[BaseApp]):
#     model: Type[BaseModel] = BaseApp
AppsPage = Page[BaseApp]


class AppPermission(BaseModel):
    name: str = Field(validation_alias=PathChoices("data.attributes.app_name"))
    access: str = Field(validation_alias=PathChoices("data.attributes.access"))


class AppPermissionsPage(Page[BaseApp]):
    model: Type[BaseModel] = BaseApp


class App(BaseApp):
    organization: str = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.organization"),
    )
    app_type: AppType = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.appType"),
    )
    urls: URLS = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.urls"),
    )
    timezone: str = Field(
        default=False,
        validation_alias=PathChoices("data.attributes.timezone"),
    )
    currency: str = Field(
        default=False,
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

    @classmethod
    def deserialize(cls, data: dict[str, Any]):
        return cls(**data)


class RequestAttributesSchema(BaseModel):
    type: str
    id: Optional[str] = Field(default=None)
    attributes: dict[str, Any]


class RequestDataSchema(BaseModel):
    data: RequestAttributesSchema

    def serialize(self) -> dict[str, Any]:
        return self.model_dump(exclude_unset=True)


@optional(exclude={"id", "type"})
class AppUpdateDraft(App):
    id: str
    type: TYPE = Field(default="ppms/app")
    name: Optional[str] = Field(default=None, max_length=90)
    urls: Optional[URLS] = Field(default=None)

    def serialize(self) -> dict[str, Any]:
        attributes = self.model_dump(exclude={"id", "type"}, exclude_unset=True)
        data = RequestAttributesSchema(id=self.id, type=self.type, attributes=attributes)
        return RequestDataSchema(data=data).serialize()


class AppCreateDraft(BaseModel):
    type: TYPE = Field(default="ppms/app")
    app_type: AppType = "web"
    name: str = Field(default=..., max_length=90)
    urls: URLS
    timezone: str = Field(
        default="UTC",
    )
    currency: str = Field(
        default="USD",
    )
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
    gdprDataAnonymizationMode: GDPR = Field(
        default="session_cookie_id",
    )
    privacyUseCookies: bool = Field(default=True)
    privacyUseFingerprinting: bool = Field(default=True)
    cnil: bool = Field(default=False)
    sessionIdStrictPrivacyMode: bool = Field(default=False)

    def serialize(self) -> dict[str, Any]:
        attributes = self.model_dump(exclude={"type"}, exclude_unset=True)
        data = RequestAttributesSchema(type=self.type, attributes=attributes)
        return RequestDataSchema(data=data).serialize()
