from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field


class Meta(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )


class ConditionMeta(Meta):
    has_abandoned_conditions: bool = Field(
        ...,
        description="Flag describing whether trigger has abandoned conditions (true), otherwise (false)",
    )

    has_conditions_with_abandoned_variable: bool = Field(
        ...,
        description="Flag describing whether trigger has condition with abandoned variable (true), otherwise (false)",
    )


class TotalMeta(Meta):
    total: int = Field(..., description="Total number of elements", ge=0)


class KeywordMeta(Meta):
    keyword: Optional[str] = None
    keyword_args: Optional[dict[str, Any]] = None
