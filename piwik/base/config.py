from __future__ import annotations

import urllib.parse

from typing import Optional

from pydantic import Field, SecretStr, ValidationInfo, field_validator
from pydantic_settings import BaseSettings, PydanticBaseSettingsSource, SettingsConfigDict


class ClientConfig(BaseSettings):
    url: str = Field(default=..., validation_alias="PIWIK_URL")
    auth_url: str = Field(default=None, validation_alias="PIWIK_AUTH_URL")
    client_id: str = Field(default=..., validation_alias="PIWIK_CLIENT_ID")
    client_secret: SecretStr = Field(default=..., validation_alias="PIWIK_CLIENT_SECRET")

    model_config = SettingsConfigDict(populate_by_name=True, env_file=".env", extra="ignore")

    @field_validator("auth_url", mode="before")
    @classmethod
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
