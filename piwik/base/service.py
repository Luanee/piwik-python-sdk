from piwik.base import BaseClient


class BaseService:
    _client: BaseClient
    _endpoint: str

    def __init__(self, client: BaseClient):
        self._client = client
