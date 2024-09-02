
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class AbandonedTag(BaseModel):
    pass


class AbandonedTagCreateDraft(TagCreateDraft):
    pass


class AbandonedTagUpdateDraft(TagUpdateDraft):
    pass

