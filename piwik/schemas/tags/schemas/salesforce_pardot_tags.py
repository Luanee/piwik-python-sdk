
from pydantic import BaseModel

from piwik.schemas.tags.base import TagCreateDraft, TagUpdateDraft


class SalesforcePardotTag(BaseModel):
    pass


class SalesforcePardotTagCreateDraft(TagCreateDraft):
    pass


class SalesforcePardotTagUpdateDraft(TagUpdateDraft):
    pass

