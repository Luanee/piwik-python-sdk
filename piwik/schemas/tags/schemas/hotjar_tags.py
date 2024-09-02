
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class HotjarTag(BaseModel):
    pass


class HotjarTagCreateDraft(TagCreateDraft):
    pass


class HotjarTagUpdateDraft(TagUpdateDraft):
    pass

