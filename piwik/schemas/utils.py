import datetime
from typing import Annotated

from pydantic import AliasChoices, AliasPath, PlainSerializer


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


class PathChoices(AliasChoices):
    def __init__(self, field: str) -> None:
        fields = field.split(".")
        paths = [AliasPath(*fields[index:]) for index, _ in enumerate(reversed(fields))]
        super().__init__(*paths)


DateString = Annotated[datetime.date, PlainSerializer(lambda x: x.strftime("%Y-%m-%d"), return_type=str)]

DateTimeString = Annotated[
    datetime.datetime, PlainSerializer(lambda x: x.strftime("%Y-%m-%dT%H:%M:%S"), return_type=str)
]
