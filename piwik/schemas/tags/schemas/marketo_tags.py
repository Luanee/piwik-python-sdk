
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class MarketoTag(BaseModel):
    pass


class MarketoTagCreateDraft(TagCreateDraft):
    pass


class MarketoTagUpdateDraft(TagUpdateDraft):
    pass

