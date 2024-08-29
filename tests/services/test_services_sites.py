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
from piwik.schemas.sites import SiteCreateDraft, SiteUpdateDraft
from tests.conftest import PIWIK_URL
from tests.data.exceptions import (
    BAD_REQUEST_EXCEPTION,
    ERROR_EXCEPTION,
    FORBIDDEN_EXCEPTION,
    GATEWAY_ERROR_EXCEPTION,
    RESOURCE_NOT_FOUND_EXCEPTION,
    SERVER_ERROR_EXCEPTION,
    UNAUTHORIZED_EXCEPTION,
)
from tests.data.sites import (
    RESPONSE_DATA_BASE_SITE,
    RESPONSE_DATA_META_SITE_APP,
    RESPONSE_DATA_SITE,
    RESPONSE_DATA_SITE_INTEGRITY_BASE,
    SITE_CREATE_DRAFT,
    SITE_UPDATE_DRAFT,
)
from tests.utils.helper import exception_handler, prepare_page_data


@pytest.fixture
def endpoint():
    yield f"{PIWIK_URL}/api/meta-sites/v1"


@pytest.mark.parametrize(
    "status_code,data,exception",
    [
        (200, prepare_page_data(RESPONSE_DATA_BASE_SITE, 0), None),
        (200, prepare_page_data(RESPONSE_DATA_BASE_SITE, 1), None),
        (200, prepare_page_data(RESPONSE_DATA_BASE_SITE, 2), None),
        (404, prepare_page_data(RESPONSE_DATA_BASE_SITE, 2), None),
        (400, BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, FORBIDDEN_EXCEPTION, ForbiddenException),
        (500, SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, ERROR_EXCEPTION, ServerErrorException),
        (503, GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_sites_list_endpoint(
    status_code: int,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("GET", re.compile(f"{endpoint}.*"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.sites.list()


@pytest.mark.parametrize(
    "status_code,id,data,exception",
    [
        (200, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 0), None),
        (200, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 1), None),
        (200, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 2), None),
        (404, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 2), None),
        (400, "id", BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, "id", UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, "id", FORBIDDEN_EXCEPTION, ForbiddenException),
        (500, "id", SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, "id", ERROR_EXCEPTION, ServerErrorException),
        (503, "id", GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_sites_list_apps_endpoint(
    status_code: int,
    id: str,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("GET", re.compile(f"{endpoint}.*"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.sites.list_apps(id)


@pytest.mark.parametrize(
    "status_code,id,data,exception",
    [
        (200, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 0), None),
        (200, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 1), None),
        (200, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 2), None),
        (404, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 2), None),
        (400, "id", BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, "id", UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, "id", FORBIDDEN_EXCEPTION, ForbiddenException),
        (500, "id", SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, "id", ERROR_EXCEPTION, ServerErrorException),
        (503, "id", GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_sites_list_all_sites_endpoint(
    status_code: int,
    id: str,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("GET", re.compile(f"{endpoint}.*"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.sites.list_all_sites(id)


@pytest.mark.parametrize(
    "status_code,id,data,exception",
    [
        (200, "1", RESPONSE_DATA_BASE_SITE, None),
        (400, "1", BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, "1", UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, "1", FORBIDDEN_EXCEPTION, ForbiddenException),
        (404, "1", RESOURCE_NOT_FOUND_EXCEPTION, ResourceNotFoundException),
        (500, "1", SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, "1", ERROR_EXCEPTION, ServerErrorException),
        (503, "1", GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_sites_get_endpoint(
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
        client.administration.sites.get(id)


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
def test_service_sites_delete_endpoint(
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
        client.administration.sites.delete(id)


@pytest.mark.parametrize(
    "status_code,draft,data,exception",
    [
        (201, SITE_CREATE_DRAFT, RESPONSE_DATA_SITE, None),
        (400, SITE_CREATE_DRAFT, BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, SITE_CREATE_DRAFT, UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, SITE_CREATE_DRAFT, FORBIDDEN_EXCEPTION, ForbiddenException),
        (500, SITE_CREATE_DRAFT, SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, SITE_CREATE_DRAFT, ERROR_EXCEPTION, ServerErrorException),
        (503, SITE_CREATE_DRAFT, GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_sites_create_endpoint(
    status_code: int,
    draft: SiteCreateDraft,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("POST", re.compile(f"{endpoint}"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.sites.create(draft)


@pytest.mark.parametrize(
    "status_code,draft,data,exception",
    [
        (204, SITE_UPDATE_DRAFT, None, None),
        (400, SITE_UPDATE_DRAFT, BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, SITE_UPDATE_DRAFT, UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, SITE_UPDATE_DRAFT, FORBIDDEN_EXCEPTION, ForbiddenException),
        (404, SITE_UPDATE_DRAFT, RESOURCE_NOT_FOUND_EXCEPTION, ResourceNotFoundException),
        (500, SITE_UPDATE_DRAFT, SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, SITE_UPDATE_DRAFT, ERROR_EXCEPTION, ServerErrorException),
        (503, SITE_UPDATE_DRAFT, GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_sites_update_endpoint(
    status_code: int,
    draft: SiteUpdateDraft,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("PATCH", re.compile(f"{endpoint}/.*"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.sites.update(draft)


@pytest.mark.parametrize(
    "status_code,id,ids,data,exception",
    [
        (204, "id", ["id_1", "id_2"], None, None),
        (400, "id", ["id_1", "id_2"], BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, "id", ["id_1", "id_2"], UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, "id", ["id_1", "id_2"], FORBIDDEN_EXCEPTION, ForbiddenException),
        (404, "id", ["id_1", "id_2"], RESOURCE_NOT_FOUND_EXCEPTION, ResourceNotFoundException),
        (500, "id", ["id_1", "id_2"], SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, "id", ["id_1", "id_2"], ERROR_EXCEPTION, ServerErrorException),
        (503, "id", ["id_1", "id_2"], GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_sites_add_apps_endpoint(
    status_code: int,
    id: str,
    ids: list[str],
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("POST", re.compile(f"{endpoint}/{id}/relationships/apps"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.sites.add_apps(id, ids)


@pytest.mark.parametrize(
    "status_code,id,ids,data,exception",
    [
        (204, "id", ["id_1", "id_2"], None, None),
        (400, "id", ["id_1", "id_2"], BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, "id", ["id_1", "id_2"], UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, "id", ["id_1", "id_2"], FORBIDDEN_EXCEPTION, ForbiddenException),
        (404, "id", ["id_1", "id_2"], RESOURCE_NOT_FOUND_EXCEPTION, ResourceNotFoundException),
        (500, "id", ["id_1", "id_2"], SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, "id", ["id_1", "id_2"], ERROR_EXCEPTION, ServerErrorException),
        (503, "id", ["id_1", "id_2"], GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_sites_delete_apps_endpoint(
    status_code: int,
    id: str,
    ids: list[str],
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri(
        "DELETE", re.compile(f"{endpoint}/{id}/relationships/apps"), status_code=status_code, json=data
    )

    with exception_handler(exception):
        client.administration.sites.delete_apps(id, ids)


@pytest.mark.parametrize(
    "status_code,id,data,exception",
    [
        (200, "1", RESPONSE_DATA_SITE_INTEGRITY_BASE, None),
        (400, "id", BAD_REQUEST_EXCEPTION, BadRequestException),
        (401, "id", UNAUTHORIZED_EXCEPTION, UnauthorizedException),
        (403, "id", FORBIDDEN_EXCEPTION, ForbiddenException),
        (404, "id", RESOURCE_NOT_FOUND_EXCEPTION, ResourceNotFoundException),
        (500, "id", SERVER_ERROR_EXCEPTION, ServerErrorException),
        (502, "id", ERROR_EXCEPTION, ServerErrorException),
        (503, "id", GATEWAY_ERROR_EXCEPTION, ServerErrorException),
    ],
)
def test_service_site_integrity_endpoint(
    status_code: int,
    id: str,
    data: dict,
    exception: Optional[Type[Exception]],
    adapter: requests_mock.Mocker,
    client: Client,
    endpoint: str,
):
    adapter.register_uri("GET", re.compile(f"{endpoint}/{id}/apps/integrity"), status_code=status_code, json=data)

    with exception_handler(exception):
        client.administration.sites.validate(id)
