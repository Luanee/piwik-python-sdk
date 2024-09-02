
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class CrazyEggTag(BaseModel):
    pass


class CrazyEggTagCreateDraft(TagCreateDraft):
    pass


class CrazyEggTagUpdateDraft(TagUpdateDraft):
    pass

