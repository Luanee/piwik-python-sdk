import contextlib
from typing import Optional, Type

import pytest


def exception_handler(
    exception: Optional[Type[Exception]] = None,
):
    if exception is None:
        context = contextlib.nullcontext()
    else:
        context = pytest.raises(exception)

    return context


def prepare_page_data(entity: dict, amount: int):
    data = [entity for i in range(amount)]

    return {
        "meta": {"total": len(data)},
        "data": data,
    }
