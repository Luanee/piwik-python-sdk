import re

import pytest
import requests_mock

from piwik.base.base_client import BaseClient
from piwik.client import Client
from piwik.services.apps import AppsService
from tests.conftest import PIWIK_URL, client


SERVICE_APP_ENDPOINT = f"{PIWIK_URL}/api/apps/v2"

APP_ID = "cb093b59-045d-47eb-8c6e-0a7fbf15b14c"


@pytest.fixture
def endpoint():
    yield f"{PIWIK_URL}/api/apps/v2"


DATA = {
    "meta": {"total": 2},
    "data": [
        {
            "type": "ppms/app",
            "id": "cb093b59-045d-47eb-8c6e-0a7fbf15b14b",
            "attributes": {
                "name": "Demo site",
                "addedAt": "2024-02-07T20:03:33+00:00",
                "updatedAt": "2024-02-07T20:03:33+00:00",
            },
        }
    ],
}


@pytest.mark.parametrize(
    "status_code,data,expatiation",
    [
        (200, DATA, 0),
    ],
)
def service(status_code: int, data: dict, expatiation, adapter: requests_mock.Mocker, client: Client, endpoint: str):
    adapter.register_uri("GET", re.compile(f"{endpoint}.*"), status_code=status_code, json=data)

    page_of_apps = client.apps.list()
    assert page_of_apps.page == 0
    assert page_of_apps.size == 10
    assert page_of_apps.total == 2
    print(page_of_apps.data)
