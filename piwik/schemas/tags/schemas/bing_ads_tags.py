
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class BingAdsTag(BaseModel):
    pass


class BingAdsTagCreateDraft(TagCreateDraft):
    pass


class BingAdsTagUpdateDraft(TagUpdateDraft):
    pass

