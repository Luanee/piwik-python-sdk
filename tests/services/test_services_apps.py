import re

from typing import Optional, Type

import pytest
import requests_mock

from piwik.client import Client
from piwik.schemas.apps import AppCreateDraft, AppUpdateDraft
from tests.conftest import PIWIK_URL, client
from tests.data.apps import (
    APP_CREATE_DRAFT,
    APP_UPDATE_DRAFT,
    RESPONSE_DATA_APP,
    RESPONSE_DATA_BASE_APP,
    RESPONSE_DATA_PERMISSION_BASE,
)
from tests.utils.helper import exception_handler, prepare_page_data


@pytest.fixture
def endpoint():
    yield f"{PIWIK_URL}/api/apps/v2"


@pytest.mark.parametrize(
    "status_code,data,exception",
    [
        (200, prepare_page_data(RESPONSE_DATA_BASE_APP, 0), None),
        (200, prepare_page_data(RESPONSE_DATA_BASE_APP, 1), None),
        (200, prepare_page_data(RESPONSE_DATA_BASE_APP, 2), None),
        (404, prepare_page_data(RESPONSE_DATA_BASE_APP, 2), None),
        (400, {"error": "BadRequest"}, ValueError),
        (401, {"error": "Unauthorized"}, ValueError),
        (403, {"error": "Forbidden"}, ValueError),
        (500, {"error": "InternalServerError"}, ValueError),
        (502, {"error": "Error"}, ValueError),
        (503, {"error": "GatewayError"}, ValueError),
    ],
)
def test_service_apps_list_endpoint(
    status_code: int,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("GET", re.compile(f"{endpoint}.*"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.apps.list()


@pytest.mark.parametrize(
    "status_code,id,data,exception",
    [
        (200, "1", RESPONSE_DATA_APP, None),
        (400, "1", {"error": "BadRequest"}, ValueError),
        (401, "1", {"error": "Unauthorized"}, ValueError),
        (403, "1", {"error": "Forbidden"}, ValueError),
        (404, "1", {"error": "ResourceNotFound"}, ValueError),
        (500, "1", {"error": "InternalServerError"}, ValueError),
        (502, "1", {"error": "Error"}, ValueError),
        (503, "1", {"error": "GatewayError"}, ValueError),
    ],
)
def test_service_apps_get_endpoint(
    status_code: int,
    id: str,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("GET", re.compile(f"{endpoint}/.*"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.apps.get(id)


@pytest.mark.parametrize(
    "status_code,id,data,exception",
    [
        (204, "1", None, None),
        (400, "1", {"error": "BadRequest"}, ValueError),
        (401, "1", {"error": "Unauthorized"}, ValueError),
        (403, "1", {"error": "Forbidden"}, ValueError),
        (404, "1", {"error": "ResourceNotFound"}, ValueError),
        (500, "1", {"error": "InternalServerError"}, ValueError),
        (502, "1", {"error": "Error"}, ValueError),
        (503, "1", {"error": "GatewayError"}, ValueError),
    ],
)
def test_service_apps_delete_endpoint(
    status_code: int,
    id: str,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("DELETE", re.compile(f"{endpoint}/.*"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.apps.delete(id)


@pytest.mark.parametrize(
    "status_code,draft,data,exception",
    [
        (201, APP_CREATE_DRAFT, RESPONSE_DATA_APP, None),
        (400, APP_CREATE_DRAFT, {"error": "BadRequest"}, ValueError),
        (401, APP_CREATE_DRAFT, {"error": "Unauthorized"}, ValueError),
        (403, APP_CREATE_DRAFT, {"error": "Forbidden"}, ValueError),
        (500, APP_CREATE_DRAFT, {"error": "InternalServerError"}, ValueError),
        (502, APP_CREATE_DRAFT, {"error": "Error"}, ValueError),
        (503, APP_CREATE_DRAFT, {"error": "GatewayError"}, ValueError),
    ],
)
def test_service_apps_create_endpoint(
    status_code: int,
    draft: AppCreateDraft,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("POST", re.compile(f"{endpoint}"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.apps.create(draft)


@pytest.mark.parametrize(
    "status_code,draft,data,exception",
    [
        (204, APP_UPDATE_DRAFT, None, None),
        (400, APP_UPDATE_DRAFT, {"error": "BadRequest"}, ValueError),
        (401, APP_UPDATE_DRAFT, {"error": "Unauthorized"}, ValueError),
        (403, APP_UPDATE_DRAFT, {"error": "Forbidden"}, ValueError),
        (404, APP_UPDATE_DRAFT, {"error": "ResourceNotFoundError"}, ValueError),
        (500, APP_UPDATE_DRAFT, {"error": "InternalServerError"}, ValueError),
        (502, APP_UPDATE_DRAFT, {"error": "Error"}, ValueError),
        (503, APP_UPDATE_DRAFT, {"error": "GatewayError"}, ValueError),
    ],
)
def test_service_apps_update_endpoint(
    status_code: int,
    draft: AppUpdateDraft,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("PATCH", re.compile(f"{endpoint}/.*"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.apps.update(draft)


@pytest.mark.parametrize(
    "status_code,id,data,exception",
    [
        (200, "1", prepare_page_data(RESPONSE_DATA_PERMISSION_BASE, 2), None),
        (400, "1", {"error": "BadRequest"}, ValueError),
        (401, "1", {"error": "Unauthorized"}, ValueError),
        (403, "1", {"error": "Forbidden"}, ValueError),
        (404, "1", {"error": "ResourceNotFoundError"}, ValueError),
        (500, "1", {"error": "InternalServerError"}, ValueError),
        (502, "1", {"error": "Error"}, ValueError),
        (503, "1", {"error": "GatewayError"}, ValueError),
    ],
)
def test_service_apps_permissions_endpoint(
    status_code: int,
    id: str,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("GET", re.compile(f"{endpoint}/user-group/.*/permissions"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.apps.permissions(id)
