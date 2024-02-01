from __future__ import annotations
from typing import Optional

import urllib.parse

from pydantic_settings import BaseSettings, SettingsConfigDict

from pydantic import Field, SecretStr, ValidationInfo, field_validator


class ClientConfig(BaseSettings):
    client_id: str = Field(default=..., alias="PIWIK_CLIENT_ID")
    client_secret: SecretStr = Field(default=..., alias="PIWIK_CLIENT_SECRET")
    url: str = Field(default="", alias="PIWIK_URL")
    auth_url: str = Field(default="", alias="PIWIK_AUTH_URL")

    model_config = SettingsConfigDict(populate_by_name=True)

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
