
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class SALESmanagoTag(BaseModel):
    pass


class SALESmanagoTagCreateDraft(TagCreateDraft):
    pass


class SALESmanagoTagUpdateDraft(TagUpdateDraft):
    pass

