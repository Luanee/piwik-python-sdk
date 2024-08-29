import datetime
from typing import Annotated, Any, Optional

from pydantic import PlainSerializer


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


def validate_comma_separated_string(parameter: str, field: Any, value: Optional[str]):
    if not value:
        return value

    valid_values = field.type_.__args__

    if all(chunk.strip() in valid_values for chunk in value.split(",")):
        return value

    raise ValueError(
        f"Parameter {parameter} should contain comma-separated strings of: {valid_values}.",
    )


DateString = Annotated[datetime.date, PlainSerializer(lambda x: x.strftime("%Y-%m-%d"), return_type=str)]

DateTimeString = Annotated[
    datetime.datetime, PlainSerializer(lambda x: x.strftime("%Y-%m-%dT%H:%M:%S"), return_type=str)
]
