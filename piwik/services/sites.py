from typing import Literal, Optional
from piwik.base.base_client import BaseClient
from piwik.services.apps import SEARCH


class SitesService:
    _client: BaseClient
    _endpoint: str = "/api/meta-sites/v1"

    def __init__(self, client: BaseClient):
        self._client = client

    def list(self):
        pass

    def get(self):
        pass

    def create(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass

    def list_apps(
        self,
        id: str,
        search: Optional[str] = None,
        sort: SEARCH = "name",
        page: int = 0,
        size: int = 10,
        type: Literal["included"] | Literal["excluded"] = "included",
    ):
        pass

    def add_apps(self):
        pass

    def delete_apps(self):
        pass

    def list_all_sites(
        self,
        search: Optional[str] = None,
        sort: SEARCH = "name",
        page: int = 0,
        size: int = 10,
        action: Literal["view"] | Literal["edit"] = "view",
    ):
        pass

    def validate(self, id: str):
        pass
