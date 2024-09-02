
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class CustomTagSynchronousDEPRECATED(BaseModel):
    pass


class CustomTagSynchronousDEPRECATEDCreateDraft(TagCreateDraft):
    pass


class CustomTagSynchronousDEPRECATEDUpdateDraft(TagUpdateDraft):
    pass

