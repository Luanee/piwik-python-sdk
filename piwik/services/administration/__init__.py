from piwik.base.base_client import BaseClient

from .apps import AppsService
from .sites import SitesService


class AdministrationServices:
    def __init__(self, client: BaseClient):
        self._client = client

    @property
    def apps(self):
        return AppsService(self._client)

    @property
    def sites(self):
        return SitesService(self._client)
