
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class MetaPixelTag(BaseModel):
    pass


class MetaPixelTagCreateDraft(TagCreateDraft):
    pass


class MetaPixelTagUpdateDraft(TagUpdateDraft):
    pass

