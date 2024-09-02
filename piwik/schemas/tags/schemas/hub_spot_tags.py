
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class HubSpotTag(BaseModel):
    pass


class HubSpotTagCreateDraft(TagCreateDraft):
    pass


class HubSpotTagUpdateDraft(TagUpdateDraft):
    pass

