from __future__ import annotations

from typing import Optional

import requests
from pydantic import BaseModel, Field, field_validator


class Source(BaseModel):
    pointer: Optional[str] = Field(default=None)
    parameter: Optional[str] = Field(default=None)


class Error(BaseModel):
    status: int
    code: Optional[str] = Field(default=None)
    title: Optional[str] = Field(default=None)
    detail: Optional[str] = Field(default=None)
    source: Optional[Source] = Field(default=None)

    @field_validator("status")
    def validate_status(cls, status: int | str):
        if isinstance(status, str):
            return int(status)
        return status


class BasePiwikException(Exception):
    status_code: int
    message: str

    def __init__(self, *, message: str, status_code: int = 500, **kwargs):
        self.status_code = status_code
        self.message = message
        self.__dict__.update(kwargs)
        super().__init__(message)

    @classmethod
    def deserialize(cls, **kwargs) -> BasePiwikException:
        return cls(**kwargs)

    def __str__(self) -> str:
        return super().__str__()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items() if v is not None)})"


class BadRequestException(BasePiwikException):
    errors: list[Error]


class ResourceNotFoundExceptions(BasePiwikException):
    status_code: int = 404

    @classmethod
    def deserialize(cls, **kwargs) -> BasePiwikException:
        message = kwargs.get("errors", [])[0]["title"]
        return cls(message=message, status_code=cls.status_code)


class ExceptionResponse(BaseModel):
    status_code: int
    message: Optional[str] = None
    errors: Optional[list[Error]] = None

    @classmethod
    def deserialize(cls, response: requests.Response) -> ExceptionResponse:
        return cls(status_code=response.status_code, **response.json())


class PiwikException:
    @classmethod
    def deserialize(cls, error: ExceptionResponse) -> BasePiwikException:
        data = error.model_dump()
        if error.status_code == 400:
            return BadRequestException.deserialize(**data)
        elif error.status_code == 404:
            return ResourceNotFoundExceptions.deserialize(**data)
        return BasePiwikException.deserialize(**data)
