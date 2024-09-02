
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class AdrollTag(BaseModel):
    pass


class AdrollTagCreateDraft(TagCreateDraft):
    pass


class AdrollTagUpdateDraft(TagUpdateDraft):
    pass

