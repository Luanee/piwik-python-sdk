from __future__ import annotations

import urllib.parse

from typing import Optional

from dotenv import load_dotenv
from pydantic import Field, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class ClientConfig(BaseSettings):
    url: str = Field(default=..., alias="PIWIK_URL")
    auth_url: str = Field(default=None, alias="PIWIK_AUTH_URL")
    client_id: str = Field(default=..., alias="PIWIK_CLIENT_ID")
    client_secret: SecretStr = Field(default=..., alias="PIWIK_CLIENT_SECRET")

    model_config = SettingsConfigDict(
        populate_by_name=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @field_validator("url", "client_id", "client_secret")
    def validate_env_variables(cls, value: Optional[str | SecretStr], info: ValidationInfo):
        """Safety"""
        if not value:
            if info.field_name in info.data:
                return info.data[info.field_name]
            raise ValueError(f"{info.field_name} should not be missing")
        return value

    @field_validator("auth_url", mode="before")
    def create_auth_url(cls, auth_url: Optional[str], info: ValidationInfo):
        """Safety"""
        if not auth_url:
            if "url" in info.data:
                return f"{info.data['url']}/auth/token"
            return None

        parts = urllib.parse.urlparse(auth_url)
        if parts.path == "":
            auth_url = urllib.parse.urlunparse((*parts[:2], "/auth/token", *parts[3:]))
        return auth_url
