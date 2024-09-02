
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class VideoHTML5Tag(BaseModel):
    pass


class VideoHTML5TagCreateDraft(TagCreateDraft):
    pass


class VideoHTML5TagUpdateDraft(TagUpdateDraft):
    pass

