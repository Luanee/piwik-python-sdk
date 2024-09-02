
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class MauticTag(BaseModel):
    pass


class MauticTagCreateDraft(TagCreateDraft):
    pass


class MauticTagUpdateDraft(TagUpdateDraft):
    pass

