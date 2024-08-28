from piwik.base.base_client import BaseClient


class TagManagerServices:
    def __init__(self, client: BaseClient):
        self._client = client
