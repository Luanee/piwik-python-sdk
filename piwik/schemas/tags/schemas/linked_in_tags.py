
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class LinkedInTag(BaseModel):
    pass


class LinkedInTagCreateDraft(TagCreateDraft):
    pass


class LinkedInTagUpdateDraft(TagUpdateDraft):
    pass

