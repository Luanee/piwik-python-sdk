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
from piwik.schemas.custom_dimensions import CustomDimensionCreateDraft, CustomDimensionUpdateDraft
from tests.conftest import PIWIK_URL
from tests.data.custom_dimensions import (
    CUSTOM_DIMENSION_CREATE_DRAFT,
    CUSTOM_DIMENSION_UPDATE_DRAFT,
    RESPONSE_DATA_CUSTOM_DIMENSION,
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
    yield f"{PIWIK_URL}/api/analytics/v1/manage/custom-dimensions"


@pytest.mark.parametrize(
    "status_code,website_id,data,exception",
    [
        (200, "website_id", prepare_page_data(RESPONSE_DATA_CUSTOM_DIMENSION, 0), None),
        (200, "website_id", prepare_page_data(RESPONSE_DATA_CUSTOM_DIMENSION, 1), None),
        (200, "website_id", prepare_page_data(RESPONSE_DATA_CUSTOM_DIMENSION, 2), None),
        (404, "website_id", prepare_page_data(RESPONSE_DATA_CUSTOM_DIMENSION, 2), None),
        (400, "website_id", BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, "website_id", UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, "website_id", FORBIDDEN_EXCEPTION, ForbiddenException),
        (500, "website_id", SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, "website_id", ERROR_EXCEPTION, ServerErrorException),
        (503, "website_id", GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_custom_dimensions_list_endpoint(
    status_code: int,
    website_id: str,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("GET", re.compile(f"{endpoint}.*"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.analytics.custom_dimensions.list(website_id)


@pytest.mark.parametrize(
    "status_code,id,website_id,data,exception",
    [
        (200, "id", "website_id", RESPONSE_DATA_CUSTOM_DIMENSION, None),
        (400, "id", "website_id", BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, "id", "website_id", UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, "id", "website_id", FORBIDDEN_EXCEPTION, ForbiddenException),
        (404, "id", "website_id", RESOURCE_NOT_FOUND_EXCEPTION, ResourceNotFoundException),
        (500, "id", "website_id", SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, "id", "website_id", ERROR_EXCEPTION, ServerErrorException),
        (503, "id", "website_id", GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_custom_dimensions_get_endpoint(
    status_code: int,
    id: str,
    website_id: str,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("GET", re.compile(f"{endpoint}/.*"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.analytics.custom_dimensions.get(id, website_id)


@pytest.mark.parametrize(
    "status_code,draft,data,exception",
    [
        (201, CUSTOM_DIMENSION_CREATE_DRAFT, RESPONSE_DATA_CUSTOM_DIMENSION, None),
        (400, CUSTOM_DIMENSION_CREATE_DRAFT, BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, CUSTOM_DIMENSION_CREATE_DRAFT, UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, CUSTOM_DIMENSION_CREATE_DRAFT, FORBIDDEN_EXCEPTION, ForbiddenException),
        (500, CUSTOM_DIMENSION_CREATE_DRAFT, SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, CUSTOM_DIMENSION_CREATE_DRAFT, ERROR_EXCEPTION, ServerErrorException),
        (503, CUSTOM_DIMENSION_CREATE_DRAFT, GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_custom_dimensions_create_endpoint(
    status_code: int,
    draft: CustomDimensionCreateDraft,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("POST", re.compile(f"{endpoint}"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.analytics.custom_dimensions.create(draft)


@pytest.mark.parametrize(
    "status_code,draft,data,exception",
    [
        (204, CUSTOM_DIMENSION_UPDATE_DRAFT, None, None),
        (400, CUSTOM_DIMENSION_UPDATE_DRAFT, BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, CUSTOM_DIMENSION_UPDATE_DRAFT, UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, CUSTOM_DIMENSION_UPDATE_DRAFT, FORBIDDEN_EXCEPTION, ForbiddenException),
        (404, CUSTOM_DIMENSION_UPDATE_DRAFT, RESOURCE_NOT_FOUND_EXCEPTION, ResourceNotFoundException),
        (500, CUSTOM_DIMENSION_UPDATE_DRAFT, SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, CUSTOM_DIMENSION_UPDATE_DRAFT, ERROR_EXCEPTION, ServerErrorException),
        (503, CUSTOM_DIMENSION_UPDATE_DRAFT, GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_custom_dimensions_update_endpoint(
    status_code: int,
    draft: CustomDimensionUpdateDraft,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("PATCH", re.compile(f"{endpoint}/.*"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.analytics.custom_dimensions.update(draft)
