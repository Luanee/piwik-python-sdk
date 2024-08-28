from piwik.base.base_client import BaseClient

from .custom_dimensions import CustomDimensionsService
from .events import EventsService
from .goals import GoalsService
from .product_custom_dimensions import ProductCustomDimensionsService
from .sessions import SessionsService
from .system_annotations import SystemAnnotationsService
from .user_annotations import UserAnnotationsService


class AnalyticsServices:
    def __init__(self, client: BaseClient):
        self._client = client

    @property
    def sessions(self):
        return SessionsService(self._client)

    @property
    def events(self):
        return EventsService(self._client)

    @property
    def goals(self):
        return GoalsService(self._client)

    @property
    def custom_dimensions(self):
        return CustomDimensionsService(self._client)

    @property
    def product_custom_dimensions(self):
        return ProductCustomDimensionsService(self._client)

    @property
    def system_annotations(self):
        return SystemAnnotationsService(self._client)

    @property
    def user_annotations(self):
        return UserAnnotationsService(self._client)
