from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class GoogleAnalyticsTag(BaseModel):
    pass


class GoogleAnalyticsTagCreateDraft(TagCreateDraft):
    pass


class GoogleAnalyticsTagUpdateDraft(TagUpdateDraft):
    pass


class GoogleAdsTrackingConversionTag(BaseModel):
    pass


class GoogleAdsTrackingConversionTagCreateDraft(TagCreateDraft):
    pass


class GoogleAdsTrackingConversionTagUpdateDraft(TagUpdateDraft):
    pass


class GoogleAdsRemarketingTag(BaseModel):
    pass


class GoogleAdsRemarketingTagCreateDraft(TagCreateDraft):
    pass


class GoogleAdsRemarketingTagUpdateDraft(TagUpdateDraft):
    pass
