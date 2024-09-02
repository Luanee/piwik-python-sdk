from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class FloodlightCounterUniqueMethodTag(BaseModel):
    pass


class FloodlightCounterUniqueMethodTagCreateDraft(TagCreateDraft):
    pass


class FloodlightCounterUniqueMethodTagUpdateDraft(TagUpdateDraft):
    pass


class FloodlightCounterStandardMethodTag(BaseModel):
    pass


class FloodlightCounterStandardMethodTagCreateDraft(TagCreateDraft):
    pass


class FloodlightCounterStandardMethodTagUpdateDraft(TagUpdateDraft):
    pass


class FloodlightCounterSessionTag(BaseModel):
    pass


class FloodlightCounterSessionTagCreateDraft(TagCreateDraft):
    pass


class FloodlightCounterSessionTagUpdateDraft(TagUpdateDraft):
    pass


class FloodlightSalesTransactionsTag(BaseModel):
    pass


class FloodlightSalesTransactionsTagCreateDraft(TagCreateDraft):
    pass


class FloodlightSalesTransactionsTagUpdateDraft(TagUpdateDraft):
    pass


class FloodlightSalesItemSoldTag(BaseModel):
    pass


class FloodlightSalesItemSoldTagCreateDraft(TagCreateDraft):
    pass


class FloodlightSalesItemSoldTagUpdateDraft(TagUpdateDraft):
    pass
