from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class PiwikPROTag(BaseModel):
    pass


class PiwikPROTagCreateDraft(TagCreateDraft):
    pass


class PiwikPROTagUpdateDraft(TagUpdateDraft):
    pass


class PiwikPROVirtualPageViewTag(BaseModel):
    pass


class PiwikPROVirtualPageViewTagCreateDraft(TagCreateDraft):
    pass


class PiwikPROVirtualPageViewTagUpdateDraft(TagUpdateDraft):
    pass


class PiwikPROGoalConversionTag(BaseModel):
    pass


class PiwikPROGoalConversionTagCreateDraft(TagCreateDraft):
    pass


class PiwikPROGoalConversionTagUpdateDraft(TagUpdateDraft):
    pass


class PiwikPROCustomEventTag(BaseModel):
    pass


class PiwikPROCustomEventTagCreateDraft(TagCreateDraft):
    pass


class PiwikPROCustomEventTagUpdateDraft(TagUpdateDraft):
    pass


class PiwikPROCustomDimensionsTag(BaseModel):
    pass


class PiwikPROCustomDimensionsTagCreateDraft(TagCreateDraft):
    pass


class PiwikPROCustomDimensionsTagUpdateDraft(TagUpdateDraft):
    pass
