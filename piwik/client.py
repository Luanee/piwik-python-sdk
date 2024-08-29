from typing import Optional

from pydantic import SecretStr
from requests.adapters import HTTPAdapter

from piwik.base import BaseClient
from piwik.base.token import BaseTokenStorage
from piwik.services.administration import AdministrationServices
from piwik.services.analytics import AnalyticsServices


class Client(BaseClient):
    def __init__(
        self,
        url: Optional[str] = None,
        auth_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str | SecretStr] = None,
        token_storage: Optional[BaseTokenStorage] = None,
        http_adapter: Optional[HTTPAdapter] = None,
    ):
        url = url or "https://{account}.piwik.pro"
        super().__init__(
            url=url,
            auth_url=auth_url,
            client_id=client_id,
            client_secret=client_secret,
            token_storage=token_storage,
            http_adapter=http_adapter,
        )

    @property
    def administration(self):
        return AdministrationServices(self)

    @property
    def analytics(self):
        return AnalyticsServices(self)
