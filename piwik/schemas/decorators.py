from typing import Callable, Optional, Type, Any, TypeVar
from copy import deepcopy

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo

TSchema = TypeVar("TSchema", bound=BaseModel)


def optional(
    model=None, include: Optional[set[str]] = None, exclude: Optional[set[str]] = None
) -> Type[TSchema] | Callable[[Type[TSchema]], Type[TSchema]]:
    exclude = exclude or set()
    include = include or set()

    def decorator(model: Type[TSchema]) -> Type[TSchema]:
        def make_field_optional(field: FieldInfo) -> tuple[Any, FieldInfo]:
            new = deepcopy(field)
            new.default = None
            new.default_factory = None
            new.annotation = Optional[field.annotation or Any]  # type: ignore
            return new.annotation, new

        fields = model.model_fields
        fields = ((k, v) for k, v in fields.items() if include and len(include) > 0 and k in include)
        fields = ((k, v) for k, v in fields if exclude and len(exclude) > 0 and k not in exclude)

        return create_model(
            model.__name__,
            __base__=model,
            __module__=model.__module__,
            **{field_name: make_field_optional(field_info) for field_name, field_info in fields},  # type: ignore
        )  # type: ignore

    if model:
        return decorator(model)
    return decorator
