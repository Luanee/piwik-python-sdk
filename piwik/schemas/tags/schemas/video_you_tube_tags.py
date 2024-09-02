
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class VideoYouTubeTag(BaseModel):
    pass


class VideoYouTubeTagCreateDraft(TagCreateDraft):
    pass


class VideoYouTubeTagUpdateDraft(TagUpdateDraft):
    pass

