import re
from typing import Optional, Type

import pytest
import requests_mock

from piwik.client import Client
from piwik.exceptions import (
    BadRequestException,
    ForbiddenException,
    ResourceNotFoundException,
    ServerErrorException,
    UnauthorizedException,
)
from piwik.schemas.apps import AppCreateDraft, AppUpdateDraft
from tests.conftest import PIWIK_URL
from tests.data.apps import (
    APP_CREATE_DRAFT,
    APP_UPDATE_DRAFT,
    RESPONSE_DATA_APP,
    RESPONSE_DATA_BASE_APP,
    RESPONSE_DATA_PERMISSION_BASE,
)
from tests.data.exceptions import (
    BAD_REQUEST_EXCEPTION,
    ERROR_EXCEPTION,
    FORBIDDEN_EXCEPTION,
    GATEWAY_ERROR_EXCEPTION,
    RESOURCE_NOT_FOUND_EXCEPTION,
    SERVER_ERROR_EXCEPTION,
    UNAUTHORIZED_EXCEPTION,
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
        (400, BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, FORBIDDEN_EXCEPTION, ForbiddenException),
        (500, SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, ERROR_EXCEPTION, ServerErrorException),
        (503, GATEWAY_ERROR_EXCEPTION, ServerErrorException),
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
        (400, "1", BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, "1", UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, "1", FORBIDDEN_EXCEPTION, ForbiddenException),
        (404, "1", RESOURCE_NOT_FOUND_EXCEPTION, ResourceNotFoundException),
        (500, "1", SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, "1", ERROR_EXCEPTION, ServerErrorException),
        (503, "1", GATEWAY_ERROR_EXCEPTION, ServerErrorException),
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
        (400, "1", BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, "1", UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, "1", FORBIDDEN_EXCEPTION, ForbiddenException),
        (404, "1", RESOURCE_NOT_FOUND_EXCEPTION, ResourceNotFoundException),
        (500, "1", SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, "1", ERROR_EXCEPTION, ServerErrorException),
        (503, "1", GATEWAY_ERROR_EXCEPTION, ServerErrorException),
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
        (400, APP_UPDATE_DRAFT, BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, APP_UPDATE_DRAFT, UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, APP_UPDATE_DRAFT, FORBIDDEN_EXCEPTION, ForbiddenException),
        (500, APP_UPDATE_DRAFT, SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, APP_UPDATE_DRAFT, ERROR_EXCEPTION, ServerErrorException),
        (503, APP_UPDATE_DRAFT, GATEWAY_ERROR_EXCEPTION, ServerErrorException),
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
        (400, APP_UPDATE_DRAFT, BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, APP_UPDATE_DRAFT, UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, APP_UPDATE_DRAFT, FORBIDDEN_EXCEPTION, ForbiddenException),
        (404, APP_UPDATE_DRAFT, RESOURCE_NOT_FOUND_EXCEPTION, ResourceNotFoundException),
        (500, APP_UPDATE_DRAFT, SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, APP_UPDATE_DRAFT, ERROR_EXCEPTION, ServerErrorException),
        (503, APP_UPDATE_DRAFT, GATEWAY_ERROR_EXCEPTION, ServerErrorException),
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
        (400, "id", BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, "id", UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, "id", FORBIDDEN_EXCEPTION, ForbiddenException),
        (404, "id", RESOURCE_NOT_FOUND_EXCEPTION, ResourceNotFoundException),
        (500, "id", SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, "id", ERROR_EXCEPTION, ServerErrorException),
        (503, "id", GATEWAY_ERROR_EXCEPTION, ServerErrorException),
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
