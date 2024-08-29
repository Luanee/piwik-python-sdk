from contextlib import nullcontext as does_not_raise
from typing import Any

import pytest
from pydantic import ValidationError

from piwik.schemas.custom_dimensions import CustomDimension, CustomDimensionCreateDraft, CustomDimensionUpdateDraft
from piwik.schemas.page import Page
from tests.data.custom_dimensions import RESPONSE_DATA_CUSTOM_DIMENSION
from tests.utils.helper import prepare_page_data


def test_deserialize_custom_dimension():
    custom_dimension = CustomDimension.deserialize(RESPONSE_DATA_CUSTOM_DIMENSION)
    assert custom_dimension.id == "id"
    assert custom_dimension.name == "Visitor hair color"
    assert custom_dimension.website_id == "website_id"


def test_deserialize_custom_dimensions_page():
    page_of_custom_dimensions = Page[CustomDimension].deserialize(
        prepare_page_data(RESPONSE_DATA_CUSTOM_DIMENSION, 2),
        page=0,
        size=3,
    )
    assert page_of_custom_dimensions.total == 2
    assert page_of_custom_dimensions.page == 0
    assert page_of_custom_dimensions.size == 3
    assert len(page_of_custom_dimensions.data) == 2
    assert repr(page_of_custom_dimensions) == "Page<CustomDimension>(page=0, size=3, total=2)"

    page_of_custom_dimensions = Page[CustomDimension].deserialize(
        prepare_page_data(RESPONSE_DATA_CUSTOM_DIMENSION, 0),
        page=0,
        size=3,
    )
    assert page_of_custom_dimensions.total == 0
    assert page_of_custom_dimensions.page == 0
    assert page_of_custom_dimensions.size == 3
    assert len(page_of_custom_dimensions.data) == 0
    assert repr(page_of_custom_dimensions) == "Page<CustomDimension>(page=0, size=3, total=0)"


@pytest.mark.parametrize(
    "draft,exception",
    [
        (
            {
                "name": "Visitor hair color",
                "website_id": "website_id",
                "active": True,
                "scope": "event",
                "slot": 1,
                "case_sensitive": True,
                "extractions": [{"target": "page_title_regex", "pattern": "pattern"}],
            },
            does_not_raise(),
        ),
        (
            {
                "name": "Visitor hair color",
                "website_id": "website_id",
                "active": True,
                "slot": 1,
                "scope": "event",
                "case_sensitive": True,
                "extractions": [],
            },
            pytest.raises(ValidationError),
        ),
        (
            {
                "name": "Visitor hair color",
                "website_id": "website_id",
                "active": True,
                "slot": 1,
                "scope": "dummy",
                "case_sensitive": True,
                "extractions": [{"target": "page_title_regex", "pattern": "pattern"}],
            },
            pytest.raises(ValidationError),
        ),
    ],
)
def test_serialize_cd_create_draft(draft: dict[str, Any], exception):
    with exception:
        cd_create_draft = CustomDimensionCreateDraft(**draft)

        cd_create_draft_serialized = cd_create_draft.serialize()

        assert cd_create_draft_serialized["data"]["type"] == cd_create_draft.type
        assert cd_create_draft_serialized["data"]["attributes"]["name"] == cd_create_draft.name
        assert cd_create_draft_serialized["data"]["attributes"]["case_sensitive"] == cd_create_draft.case_sensitive


@pytest.mark.parametrize(
    "draft,exception",
    [
        (
            {
                "id": "id",
                "name": "Visitor hair color",
                "website_id": "website_id",
                "active": True,
                "scope": "event",
                "case_sensitive": True,
                "extractions": [{"target": "page_title_regex", "pattern": "pattern"}],
            },
            does_not_raise(),
        ),
        (
            {
                "id": None,
                "name": "Visitor hair color",
                "website_id": "website_id",
                "active": True,
                "scope": "event",
                "case_sensitive": True,
                "extractions": [],
            },
            pytest.raises(ValidationError),
        ),
        (
            {
                "id": "id",
                "name": "Visitor hair color",
                "website_id": "website_id",
                "active": True,
                "scope": "dummy",
                "case_sensitive": True,
                "extractions": [{"target": "page_title_regex", "pattern": "pattern"}],
            },
            pytest.raises(ValidationError),
        ),
        (
            {
                "id": None,
                "name": "Visitor hair color",
                "website_id": "website_id",
                "active": True,
                "scope": "event",
                "case_sensitive": True,
                "extractions": 1,
            },
            pytest.raises(ValidationError),
        ),
    ],
)
def test_serialize_cd_update_draft(draft: dict[str, Any], exception):
    with exception:
        cd_update_draft = CustomDimensionUpdateDraft(**draft)

        cd_update_draft_serialized = cd_update_draft.serialize()

        assert cd_update_draft_serialized["data"]["id"] == cd_update_draft.id
        assert cd_update_draft_serialized["data"]["type"] == cd_update_draft.type
        assert cd_update_draft_serialized["data"]["attributes"]["name"] == cd_update_draft.name
        assert cd_update_draft_serialized["data"]["attributes"]["case_sensitive"] == cd_update_draft.case_sensitive
