
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class OptimizelyTagDEPRECATED(BaseModel):
    pass


class OptimizelyTagDEPRECATEDCreateDraft(TagCreateDraft):
    pass


class OptimizelyTagDEPRECATEDUpdateDraft(TagUpdateDraft):
    pass

