
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class ABTastyTagDEPRECATED(BaseModel):
    pass


class ABTastyTagDEPRECATEDCreateDraft(TagCreateDraft):
    pass


class ABTastyTagDEPRECATEDUpdateDraft(TagUpdateDraft):
    pass

