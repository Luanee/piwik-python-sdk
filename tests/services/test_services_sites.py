import re

from typing import Optional, Type

import pytest
import requests_mock

from piwik.client import Client
from piwik.schemas.sites import SiteCreateDraft, SiteUpdateDraft
from tests.conftest import PIWIK_URL, client
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
        (400, {"error": "BadRequest"}, ValueError),
        (401, {"error": "Unauthorized"}, ValueError),
        (403, {"error": "Forbidden"}, ValueError),
        (500, {"error": "InternalServerError"}, ValueError),
        (502, {"error": "Error"}, ValueError),
        (503, {"error": "GatewayError"}, ValueError),
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
        client.sites.list()


@pytest.mark.parametrize(
    "status_code,id,data,exception",
    [
        (200, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 0), None),
        (200, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 1), None),
        (200, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 2), None),
        (404, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 2), None),
        (400, "id", {"error": "BadRequest"}, ValueError),
        (401, "id", {"error": "Unauthorized"}, ValueError),
        (403, "id", {"error": "Forbidden"}, ValueError),
        (500, "id", {"error": "InternalServerError"}, ValueError),
        (502, "id", {"error": "Error"}, ValueError),
        (503, "id", {"error": "GatewayError"}, ValueError),
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
        client.sites.list_apps(id)


@pytest.mark.parametrize(
    "status_code,id,data,exception",
    [
        (200, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 0), None),
        (200, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 1), None),
        (200, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 2), None),
        (404, "id", prepare_page_data(RESPONSE_DATA_META_SITE_APP, 2), None),
        (400, "id", {"error": "BadRequest"}, ValueError),
        (401, "id", {"error": "Unauthorized"}, ValueError),
        (403, "id", {"error": "Forbidden"}, ValueError),
        (500, "id", {"error": "InternalServerError"}, ValueError),
        (502, "id", {"error": "Error"}, ValueError),
        (503, "id", {"error": "GatewayError"}, ValueError),
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
        client.sites.list_all_sites(id)


@pytest.mark.parametrize(
    "status_code,id,data,exception",
    [
        (200, "1", RESPONSE_DATA_BASE_SITE, None),
        (400, "1", {"error": "BadRequest"}, ValueError),
        (401, "1", {"error": "Unauthorized"}, ValueError),
        (403, "1", {"error": "Forbidden"}, ValueError),
        (404, "1", {"error": "ResourceNotFound"}, ValueError),
        (500, "1", {"error": "InternalServerError"}, ValueError),
        (502, "1", {"error": "Error"}, ValueError),
        (503, "1", {"error": "GatewayError"}, ValueError),
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
        client.sites.get(id)


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
        client.sites.delete(id)


@pytest.mark.parametrize(
    "status_code,draft,data,exception",
    [
        (201, SITE_CREATE_DRAFT, RESPONSE_DATA_SITE, None),
        (400, SITE_CREATE_DRAFT, {"error": "BadRequest"}, ValueError),
        (401, SITE_CREATE_DRAFT, {"error": "Unauthorized"}, ValueError),
        (403, SITE_CREATE_DRAFT, {"error": "Forbidden"}, ValueError),
        (500, SITE_CREATE_DRAFT, {"error": "InternalServerError"}, ValueError),
        (502, SITE_CREATE_DRAFT, {"error": "Error"}, ValueError),
        (503, SITE_CREATE_DRAFT, {"error": "GatewayError"}, ValueError),
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
        client.sites.create(draft)


@pytest.mark.parametrize(
    "status_code,draft,data,exception",
    [
        (204, SITE_UPDATE_DRAFT, None, None),
        (400, SITE_UPDATE_DRAFT, {"error": "BadRequest"}, ValueError),
        (401, SITE_UPDATE_DRAFT, {"error": "Unauthorized"}, ValueError),
        (403, SITE_UPDATE_DRAFT, {"error": "Forbidden"}, ValueError),
        (404, SITE_UPDATE_DRAFT, {"error": "ResourceNotFoundError"}, ValueError),
        (500, SITE_UPDATE_DRAFT, {"error": "InternalServerError"}, ValueError),
        (502, SITE_UPDATE_DRAFT, {"error": "Error"}, ValueError),
        (503, SITE_UPDATE_DRAFT, {"error": "GatewayError"}, ValueError),
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
        client.sites.update(draft)


@pytest.mark.parametrize(
    "status_code,id,ids,data,exception",
    [
        (204, "id", ["id_1", "id_2"], None, None),
        (400, "id", ["id_1", "id_2"], {"error": "BadRequest"}, ValueError),
        (401, "id", ["id_1", "id_2"], {"error": "Unauthorized"}, ValueError),
        (403, "id", ["id_1", "id_2"], {"error": "Forbidden"}, ValueError),
        (404, "id", ["id_1", "id_2"], {"error": "ResourceNotFoundError"}, ValueError),
        (500, "id", ["id_1", "id_2"], {"error": "InternalServerError"}, ValueError),
        (502, "id", ["id_1", "id_2"], {"error": "Error"}, ValueError),
        (503, "id", ["id_1", "id_2"], {"error": "GatewayError"}, ValueError),
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
        client.sites.add_apps(id, ids)


@pytest.mark.parametrize(
    "status_code,id,ids,data,exception",
    [
        (204, "id", ["id_1", "id_2"], None, None),
        (400, "id", ["id_1", "id_2"], {"error": "BadRequest"}, ValueError),
        (401, "id", ["id_1", "id_2"], {"error": "Unauthorized"}, ValueError),
        (403, "id", ["id_1", "id_2"], {"error": "Forbidden"}, ValueError),
        (404, "id", ["id_1", "id_2"], {"error": "ResourceNotFoundError"}, ValueError),
        (500, "id", ["id_1", "id_2"], {"error": "InternalServerError"}, ValueError),
        (502, "id", ["id_1", "id_2"], {"error": "Error"}, ValueError),
        (503, "id", ["id_1", "id_2"], {"error": "GatewayError"}, ValueError),
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
        client.sites.delete_apps(id, ids)


@pytest.mark.parametrize(
    "status_code,id,data,exception",
    [
        (200, "1", RESPONSE_DATA_SITE_INTEGRITY_BASE, None),
        (400, "1", {"error": "BadRequest"}, ValueError),
        (401, "1", {"error": "Unauthorized"}, ValueError),
        (403, "1", {"error": "Forbidden"}, ValueError),
        (404, "1", {"error": "ResourceNotFoundError"}, ValueError),
        (500, "1", {"error": "InternalServerError"}, ValueError),
        (502, "1", {"error": "Error"}, ValueError),
        (503, "1", {"error": "GatewayError"}, ValueError),
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
        client.sites.validate(id)
