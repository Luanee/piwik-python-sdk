
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class ClicktaleTagDEPRECATED(BaseModel):
    pass


class ClicktaleTagDEPRECATEDCreateDraft(TagCreateDraft):
    pass


class ClicktaleTagDEPRECATEDUpdateDraft(TagUpdateDraft):
    pass

