
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class VisualWebsiteOptimizerTagDEPRECATED(BaseModel):
    pass


class VisualWebsiteOptimizerTagDEPRECATEDCreateDraft(TagCreateDraft):
    pass


class VisualWebsiteOptimizerTagDEPRECATEDUpdateDraft(TagUpdateDraft):
    pass

