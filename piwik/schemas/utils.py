import inspect
import pprint

from typing import Callable, Optional, Type

from pydantic import AliasChoices, AliasPath, BaseModel


def urls_startswith(urls: list[str]):
    if all(
        url.startswith(
            "http://",
        )
        or url.startswith(
            "https://",
        )
        for url in urls
    ):
        return urls
    raise ValueError(
        "URLs should start with one of: 'http://' or 'https://'.",
    )


from copy import deepcopy
from typing import Any, Callable, Optional, TypeVar

from pydantic import BaseModel, create_model
from pydantic.fields import FieldInfo


T = TypeVar("T", bound="BaseModel")


def optional(
    _cls=None,
    include: Optional[set[str]] = None,
    exclude: Optional[set[str]] = None,
) -> Callable[[type[T]], type[T]]:
    """Return a decorator to make model fields optional"""

    if exclude is None:
        exclude = set()

    def decorator(model: type[T]) -> type[T]:
        def make_optional(field: FieldInfo, default: Any = None) -> tuple[Any, FieldInfo]:
            new = deepcopy(field)
            new.default = default
            new.annotation = Optional[field.annotation or Any]
            return new.annotation, new

        fields = model.model_fields
        if include is None:
            fields = fields.items()
        else:
            fields = ((k, v) for k, v in fields.items() if k in include)

        return create_model(
            f"Partial{model.__name__}",
            __base__=model,
            __module__=model.__module__,
            **{
                field_name: make_optional(field_info)
                for field_name, field_info in fields
                if (exclude is None or field_name not in exclude)
            },  # type: ignore
        )

    if _cls:
        return decorator(_cls)

    return decorator


class PathChoices(AliasChoices):
    def __init__(self, field: str) -> None:
        fields = field.split(".")
        paths = [AliasPath(*fields[index:]) for index, _ in enumerate(reversed(fields))]
        super().__init__(*paths)
