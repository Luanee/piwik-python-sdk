
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class CookieInformationCMPIntegrationTag(BaseModel):
    pass


class CookieInformationCMPIntegrationTagCreateDraft(TagCreateDraft):
    pass


class CookieInformationCMPIntegrationTagUpdateDraft(TagUpdateDraft):
    pass

