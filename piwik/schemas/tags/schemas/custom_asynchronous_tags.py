from typing import Any, Optional

from pydantic import Field

from piwik.schemas.tags.base import Tag, TagCreateDraft, TagUpdateDraft
from scrape.JSON_API_1 import Scheduler


class CustomTagAsynchronous(Tag):
    disable_in_debug_mode: bool = Field(
        ...,
        description="Flag describing whether tag should be disabled in debug mode (true) or enabled (false)",
    )
    document_write: bool = Field(
        ...,
        description="Flag describing whether tag is using JavaScripts document.write method (true) or not (false)",
    )
    respect_visitors_privacy: bool = Field(
        ...,
        description="Flag describing whether tag should respect visitors privacy settings (DNT header, opt-out)",
    )
    scheduler: Scheduler = Field(..., description="Tag flight date and time definition")
    template_options: dict[str, Any] = Field(..., description="[Tag template options](#tag-template-options)")


class CustomTagAsynchronousCreateDraft(TagCreateDraft):
    disable_in_debug_mode: Optional[bool] = Field(
        default=False,
        description="Flag describing whether tag should be disabled in debug mode (true) or enabled (false)",
    )
    document_write: Optional[bool] = Field(
        default=False,
        description="Flag describing whether tag is using JavaScripts document.write method (true) or not (false)",
    )
    respect_visitors_privacy: Optional[bool] = Field(
        default=True,
        description="Flag describing whether tag should respect visitors privacy settings (DNT header, opt-out)",
    )
    scheduler: Optional[Scheduler] = Field(default=None, description="Tag flight date and time definition")


class CustomTagAsynchronousUpdateDraft(TagUpdateDraft):
    pass
