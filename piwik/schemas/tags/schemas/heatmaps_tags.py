
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class HeatmapsTag(BaseModel):
    pass


class HeatmapsTagCreateDraft(TagCreateDraft):
    pass


class HeatmapsTagUpdateDraft(TagUpdateDraft):
    pass

