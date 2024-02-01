from typing import Optional

from pywik.base import BaseClient
from pywik.base.token import BaseTokenStorage
from requests.adapters import HTTPAdapter

from pywik.services.apps import AppsService


class Client(BaseClient):
    def __init__(
        self,
        url: Optional[str] = None,
        auth_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
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
    def apps(self):
        return AppsService(self)
