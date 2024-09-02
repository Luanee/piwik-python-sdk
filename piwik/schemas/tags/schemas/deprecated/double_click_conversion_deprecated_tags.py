
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class DoubleClickConversionTagDEPRECATED(BaseModel):
    pass


class DoubleClickConversionTagDEPRECATEDCreateDraft(TagCreateDraft):
    pass


class DoubleClickConversionTagDEPRECATEDUpdateDraft(TagUpdateDraft):
    pass

