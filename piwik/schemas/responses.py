from typing import Optional

from pydantic import AnyUrl, BaseModel, ConfigDict, Field

from piwik.schemas.meta import TotalMeta


class Links(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    test: int
    test_2: int = 1

    self: AnyUrl = Field(..., description="Link to current page")
    self2: Optional[AnyUrl] = Field(None, description="Link to current page")
    first: Optional[AnyUrl] = Field(default=None, description="Link to first page")
    last: Optional[AnyUrl] = Field(default=None, description="Link to last page")
    prev: Optional[AnyUrl] = Field(default=None, description="Link to previous page")
    next: Optional[AnyUrl] = Field(default=None, description="Link to next page")


class ApiResponse(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )
    data: list[str] = Field(..., title="JSON:API 1.0 list response data")
    meta: TotalMeta = Field(..., description="Meta information about resources")
    links: Links = Field(..., description="Pagination links")


class ApiErrorResponse(BaseModel):
    pass
