from typing import Literal, Optional, get_args

from pydantic import Field

from piwik.schemas.base import (
    BaseSchema,
    CreateRequestDataMixin,
    UpdateRequestDataMixin,
)
from piwik.schemas.types import PathChoices

GoalType = Literal["Goal"]
GOAL_TYPE: GoalType = get_args(GoalType)[0]

TriggerTypes = (
    Literal["url"]
    | Literal["title"]
    | Literal["event_name"]
    | Literal["event_category"]
    | Literal["event_action"]
    | Literal["file"]
    | Literal["external_website"]
    | Literal["manually"]
)

PatternTypes = Literal["contains"] | Literal["exact"] | Literal["regex"]


class Goal(BaseSchema):
    __repr_fields__: set[str] = {"id", "name"}

    type: GoalType = Field(default=GOAL_TYPE)

    website_id: str = Field(
        validation_alias=PathChoices("data.attributes.website_id"),
    )
    name: str = Field(
        validation_alias=PathChoices("data.attributes.name"),
    )
    description: Optional[str] = Field(
        default=None,
        validation_alias=PathChoices("data.attributes.description"),
    )
    trigger: TriggerTypes = Field(
        validation_alias=PathChoices("data.attributes.trigger"),
    )
    pattern: Optional[str] = Field(
        default=None,
        validation_alias=PathChoices("data.attributes.pattern"),
    )
    pattern_type: Optional[PatternTypes] = Field(
        default=None,
        validation_alias=PathChoices("data.attributes.pattern_type"),
    )
    allow_multiple: bool = Field(
        validation_alias=PathChoices("data.attributes.allow_multiple"),
    )
    case_sensitive: bool = Field(
        validation_alias=PathChoices("data.attributes.case_sensitive"),
    )
    revenue: float = Field(
        validation_alias=PathChoices("data.attributes.revenue"),
    )


class GoalUpdateDraft(UpdateRequestDataMixin, Goal):
    id: str
    type: GoalType = Field(default=GOAL_TYPE)
    website_id: str
    name: str
    description: Optional[str] = Field(default=None)
    trigger: TriggerTypes
    pattern: Optional[str] = Field(default=None)
    pattern_type: Optional[PatternTypes] = Field(default=None)
    allow_multiple: Optional[str] = Field(default=None)
    case_sensitive: Optional[str] = Field(default=None)
    revenue: float


class GoalCreateDraft(CreateRequestDataMixin, Goal):
    id: None = None
