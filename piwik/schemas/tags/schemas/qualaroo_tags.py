
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class QualarooTag(BaseModel):
    pass


class QualarooTagCreateDraft(TagCreateDraft):
    pass


class QualarooTagUpdateDraft(TagUpdateDraft):
    pass

