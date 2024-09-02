
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class CustomContent(BaseModel):
    pass


class CustomContentCreateDraft(TagCreateDraft):
    pass


class CustomContentUpdateDraft(TagUpdateDraft):
    pass

