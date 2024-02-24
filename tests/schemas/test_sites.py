from contextlib import nullcontext as does_not_raise
from typing import Any

import pytest

from pydantic import ValidationError

from piwik.schemas.base import BaseSite
from piwik.schemas.page import Page
from piwik.schemas.sites import Site, SiteContainer, SiteCreateDraft, SiteIntegrity, SiteUpdateDraft
from tests.data.apps import RESPONSE_DATA_APP, RESPONSE_DATA_BASE_APP, RESPONSE_DATA_PERMISSION_BASE
from tests.data.sites import RESPONSE_DATA_SITE_INTEGRITY_BASE
from tests.utils.helper import prepare_page_data


def test_deserialize_site():
    site = Site.deserialize(RESPONSE_DATA_APP)
    assert site.id == "cb093b59-045d-47eb-8c6e-0a7fbf15b14b"
    assert site.name == "Demo site"
    assert site.currency == "USD"


def test_deserialize_sites_page():
    page_of_sites = Page[BaseSite].deserialize(
        prepare_page_data(RESPONSE_DATA_BASE_APP, 2),
        page=0,
        size=3,
    )
    assert page_of_sites.total == 2
    assert page_of_sites.page == 0
    assert page_of_sites.size == 3
    assert len(page_of_sites.data) == 2
    assert repr(page_of_sites) == "Page<BaseSite>(page=0, size=3, total=2)"

    page_of_sites = Page[BaseSite].deserialize(
        prepare_page_data(RESPONSE_DATA_BASE_APP, 0),
        page=0,
        size=3,
    )
    assert page_of_sites.total == 0
    assert page_of_sites.page == 0
    assert page_of_sites.size == 3
    assert len(page_of_sites.data) == 0
    assert repr(page_of_sites) == "Page<BaseSite>(page=0, size=3, total=0)"


@pytest.mark.parametrize(
    "draft,exception",
    [
        ({"name": "Demo Site 3"}, does_not_raise()),
        ({"name": "Demo Site 3", "e_commerce_tracking": "e_commerce_tracking"}, pytest.raises(ValidationError)),
        ({"name": "Demo Site 3", "type": "sites"}, pytest.raises(ValidationError)),
    ],
)
def test_serialize_site_create_draft(draft: dict[str, Any], exception):
    with exception as e:
        site_create_draft = SiteCreateDraft(**draft)

        site_create_draft_serialized = site_create_draft.serialize()

        assert site_create_draft_serialized["data"]["type"] == site_create_draft.type
        assert site_create_draft_serialized["data"]["attributes"]["name"] == site_create_draft.name


@pytest.mark.parametrize(
    "draft,exception",
    [
        (
            {"id": "id", "name": "Demo Site 3"},
            does_not_raise(),
        ),
        (
            {"id": "id", "name": "Demo Site 3", "e_commerce_tracking": "e_commerce_tracking"},
            pytest.raises(ValidationError),
        ),
        (
            {"id": "id", "name": "Demo Site 3", "type": "sites"},
            pytest.raises(ValidationError),
        ),
    ],
)
def test_serialize_site_update_draft(draft: dict[str, Any], exception):
    with exception as e:
        site_update_draft = SiteUpdateDraft(**draft)

        site_update_draft_serialized = site_update_draft.serialize()

        assert site_update_draft_serialized["data"]["id"] == site_update_draft.id
        assert site_update_draft_serialized["data"]["type"] == site_update_draft.type
        assert site_update_draft_serialized["data"]["attributes"]["name"] == site_update_draft.name


def test_serialize_site_integrity():
    site_integrity = SiteIntegrity.deserialize(RESPONSE_DATA_SITE_INTEGRITY_BASE)
    assert site_integrity.type == "meta-site/apps/integrity"
    assert site_integrity.is_currency_valid == True
    assert site_integrity.is_timezone_valid == False


def test_serialize_site_container():
    site_container = SiteContainer(ids=["id_1", "id_2"])
    assert site_container.type == "ppms/app"
    assert len(site_container.ids) == 2

    data = site_container.serialize()

    assert isinstance(data, dict)
    assert len(data["data"]) == 2
    assert data["data"][0]["id"] == "id_1"
    assert data["data"][1]["id"] == "id_2"
