from contextlib import nullcontext as does_not_raise
from typing import Any

import pytest
from pydantic import ValidationError

from piwik.schemas.apps import App, AppCreateDraft, AppPermission, AppUpdateDraft
from piwik.schemas.base import BaseSite
from piwik.schemas.page import Page
from tests.data.apps import RESPONSE_DATA_APP, RESPONSE_DATA_BASE_APP, RESPONSE_DATA_PERMISSION_BASE
from tests.utils.helper import prepare_page_data


def test_deserialize_app():
    app = App.deserialize(RESPONSE_DATA_APP)
    assert app.id == "cb093b59-045d-47eb-8c6e-0a7fbf15b14b"
    assert app.name == "Demo site"
    assert app.currency == "USD"


def test_deserialize_apps_page():
    page_of_apps = Page[BaseSite].deserialize(
        prepare_page_data(RESPONSE_DATA_BASE_APP, 2),
        page=0,
        size=3,
    )
    assert page_of_apps.total == 2
    assert page_of_apps.page == 0
    assert page_of_apps.size == 3
    assert len(page_of_apps.data) == 2
    assert repr(page_of_apps) == "Page<BaseSite>(page=0, size=3, total=2)"

    page_of_apps = Page[BaseSite].deserialize(
        prepare_page_data(RESPONSE_DATA_BASE_APP, 0),
        page=0,
        size=3,
    )
    assert page_of_apps.total == 0
    assert page_of_apps.page == 0
    assert page_of_apps.size == 3
    assert len(page_of_apps.data) == 0
    assert repr(page_of_apps) == "Page<BaseSite>(page=0, size=3, total=0)"


@pytest.mark.parametrize(
    "draft,exception",
    [
        ({"name": "Demo Site 3", "urls": ["https://demosite3.com"]}, does_not_raise()),
        ({"name": "Demo Site 3", "urls": ["demosite3.com"]}, pytest.raises(ValidationError)),
        ({"name": "Demo Site 3", "urls": ["https://demosite3.com"], "type": "apps"}, pytest.raises(ValidationError)),
    ],
)
def test_serialize_app_create_draft(draft: dict[str, Any], exception):
    with exception:
        app_create_draft = AppCreateDraft(**draft)

        app_create_draft_serialized = app_create_draft.serialize()

        assert app_create_draft_serialized["data"]["type"] == app_create_draft.type
        assert app_create_draft_serialized["data"]["attributes"]["name"] == app_create_draft.name
        assert app_create_draft_serialized["data"]["attributes"]["urls"] == app_create_draft.urls


@pytest.mark.parametrize(
    "draft,exception",
    [
        (
            {"id": "id", "name": "Demo Site 3", "urls": ["https://demosite3.com"]},
            does_not_raise(),
        ),
        (
            {"id": "id", "name": "Demo Site 3", "urls": ["demosite3.com"]},
            pytest.raises(ValidationError),
        ),
        (
            {"id": "id", "name": "Demo Site 3", "urls": ["https://demosite3.com"], "type": "apps"},
            pytest.raises(ValidationError),
        ),
        (
            {"id": None, "name": "Demo Site 3", "urls": ["https://demosite3.com"], "type": "apps"},
            pytest.raises(ValidationError),
        ),
    ],
)
def test_serialize_app_update_draft(draft: dict[str, Any], exception):
    with exception as e:
        app_update_draft = AppUpdateDraft(**draft)

        app_update_draft_serialized = app_update_draft.serialize()

        assert app_update_draft_serialized["data"]["id"] == app_update_draft.id
        assert app_update_draft_serialized["data"]["type"] == app_update_draft.type
        assert app_update_draft_serialized["data"]["attributes"]["name"] == app_update_draft.name
        assert app_update_draft_serialized["data"]["attributes"]["urls"] == app_update_draft.urls


def test_serialize_app_permission():
    page_of_app_permissions = Page[AppPermission].deserialize(
        prepare_page_data(RESPONSE_DATA_PERMISSION_BASE, 2),
        page=0,
        size=3,
    )
    assert page_of_app_permissions.total == 2
    assert page_of_app_permissions.page == 0
    assert page_of_app_permissions.size == 3
    assert len(page_of_app_permissions.data) == 2
    assert repr(page_of_app_permissions) == "Page<AppPermission>(page=0, size=3, total=2)"

    page_of_app_permissions = Page[AppPermission].deserialize(
        prepare_page_data(RESPONSE_DATA_PERMISSION_BASE, 0),
        page=0,
        size=3,
    )
    assert page_of_app_permissions.total == 0
    assert page_of_app_permissions.page == 0
    assert page_of_app_permissions.size == 3
    assert len(page_of_app_permissions.data) == 0
    assert repr(page_of_app_permissions) == "Page<AppPermission>(page=0, size=3, total=0)"
