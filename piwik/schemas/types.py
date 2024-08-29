from __future__ import annotations

from enum import Enum
from typing import Any, Literal, Optional

from pydantic import AliasChoices, AliasPath, BaseModel

RELATIVE_DATE = (
    Literal["today"]
    | Literal["yesterday"]
    | Literal["last_week"]
    | Literal["last_month"]
    | Literal["last_year"]
    | Literal["last_x_days"]
    | str
)


FORMAT = Literal["json"] | Literal["json-kv"] | Literal["csv"]
COLUMN_FORMAT = Literal["id"] | Literal["name"]


class FilterOperator(Enum):
    EQ = ("eq",)
    NEQ = ("neq",)
    CONTAINS = ("contains",)
    NOT_CONTAINS = ("not_contains",)
    ICONTAINS = ("icontains",)
    NOT_ICONTAINS = ("not_icontains",)
    STARTS_WITH = ("starts_with",)
    ENDS_WITH = ("ends_with",)
    MATCHES = ("matches",)
    NOT_MATCHES = ("not_matches",)
    GT = ("gt",)
    GTE = ("gte",)
    LT = ("lt",)
    LTE = ("lte",)
    EMPTY = ("empty",)
    NOT_EMPTY = "not_empty"


class LogicOperator(Enum):
    AND = "and"
    OR = "or"


class PathChoices(AliasChoices):
    def __init__(self, field: str, *choices: str) -> None:
        paths = []

        for choice in [field, *choices]:
            fields = choice.split(".")
            paths.extend(AliasPath(*fields[index:]) for index, _ in enumerate(reversed(fields)))

        super().__init__(*paths)


class Column(BaseModel):
    column_id: str
    transformation_id: Optional[str] = None
    goal_id: Optional[str] = None

    @classmethod
    def create(cls, data: str | dict[str, Any] | Column) -> Column:
        if isinstance(data, Column):
            return Column(**data.model_dump())
        elif isinstance(data, dict):
            return Column(**data)
        elif isinstance(data, str):
            return Column(column_id=data)


class Condition(BaseModel):
    operator: FilterOperator
    value: Any


class Filter(BaseModel):
    column_id: str
    transformation_id: Optional[str] = None
    condition: Condition


class FilterCondition(BaseModel):
    operator: LogicOperator
    conditions: list[Filter | FilterCondition]
