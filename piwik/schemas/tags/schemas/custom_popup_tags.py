
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class CustomPopup(BaseModel):
    pass


class CustomPopupCreateDraft(TagCreateDraft):
    pass


class CustomPopupUpdateDraft(TagUpdateDraft):
    pass

