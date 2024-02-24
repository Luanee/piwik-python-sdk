from typing import Optional

from requests.adapters import HTTPAdapter

from piwik.base import BaseClient
from piwik.base.token import BaseTokenStorage
from piwik.services.apps import AppsService
from piwik.services.sites import SitesService


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

    @property
    def sites(self):
        return SitesService(self)
