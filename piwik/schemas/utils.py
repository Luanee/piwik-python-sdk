import datetime
from typing import Annotated, Any, Optional

from pydantic import AfterValidator, PlainSerializer


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


def parse_date(value: str | datetime.date) -> datetime.date:
    if isinstance(value, datetime.date):
        return value
    return datetime.datetime.strptime(value, "%Y-%m-%d").date()


def parse_time(value: str | datetime.time) -> datetime.time:
    if isinstance(value, datetime.time):
        return value
    return datetime.datetime.strptime(value, "%H:%M:%S").time()


def parse_datetime(value: str | datetime.datetime) -> datetime.datetime:
    if isinstance(value, datetime.datetime):
        return value
    return datetime.datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")


DateString = Annotated[
    datetime.date,
    AfterValidator(parse_date),
    PlainSerializer(lambda x: x.strftime("%Y-%m-%d"), return_type=str),
]

TimeString = Annotated[
    datetime.time,
    AfterValidator(parse_time),
    PlainSerializer(lambda x: x.strftime("%H:%M:%S"), return_type=str),
]

DateTimeString = Annotated[
    datetime.datetime,
    AfterValidator(parse_datetime),
    PlainSerializer(lambda x: x.strftime("%Y-%m-%dT%H:%M:%S"), return_type=str),
]
