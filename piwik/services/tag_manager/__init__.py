from piwik.base.base_client import BaseClient
from piwik.services.tag_manager.tags import TagsService


class TagManagerServices:
    def __init__(self, client: BaseClient):
        self._client = client

    @property
    def tags(self):
        return TagsService(self._client)
