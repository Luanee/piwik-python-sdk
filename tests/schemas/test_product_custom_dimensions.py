from contextlib import nullcontext as does_not_raise
from typing import Any

import pytest
from pydantic import ValidationError

from piwik.schemas.page import Page
from piwik.schemas.product_custom_dimensions import (
    ProductCustomDimension,
    ProductCustomDimensionCreateDraft,
    ProductCustomDimensionUpdateDraft,
)
from tests.data.product_custom_dimensions import RESPONSE_DATA_PRODUCT_CUSTOM_DIMENSION
from tests.utils.helper import prepare_page_data


def test_deserialize_pcd():
    pcd = ProductCustomDimension.deserialize(RESPONSE_DATA_PRODUCT_CUSTOM_DIMENSION)
    assert pcd.id == "id"
    assert pcd.name == "Product package height in mm"
    assert pcd.website_id == "website_id"


def test_deserialize_pcds_page():
    page_of_pcds = Page[ProductCustomDimension].deserialize(
        prepare_page_data(RESPONSE_DATA_PRODUCT_CUSTOM_DIMENSION, 2),
        page=0,
        size=3,
    )
    assert page_of_pcds.total == 2
    assert page_of_pcds.page == 0
    assert page_of_pcds.size == 3
    assert len(page_of_pcds.data) == 2
    assert repr(page_of_pcds) == "Page<ProductCustomDimension>(page=0, size=3, total=2)"

    page_of_pcds = Page[ProductCustomDimension].deserialize(
        prepare_page_data(RESPONSE_DATA_PRODUCT_CUSTOM_DIMENSION, 0),
        page=0,
        size=3,
    )
    assert page_of_pcds.total == 0
    assert page_of_pcds.page == 0
    assert page_of_pcds.size == 3
    assert len(page_of_pcds.data) == 0
    assert repr(page_of_pcds) == "Page<ProductCustomDimension>(page=0, size=3, total=0)"


@pytest.mark.parametrize(
    "draft,exception",
    [
        (
            {
                "name": "Product package height in mm",
                "website_id": "website_id",
                "slot": 1,
            },
            does_not_raise(),
        ),
        (
            {
                "name": "Product package height in mm",
                "website_id": "website_id",
                "slot": "de 1",
            },
            pytest.raises(ValidationError),
        ),
        (
            {
                "name": "Product package height in mm",
                "website_id": "website_id",
            },
            pytest.raises(ValidationError),
        ),
    ],
)
def test_serialize_pcd_create_draft(draft: dict[str, Any], exception):
    with exception:
        pcd_create_draft = ProductCustomDimensionCreateDraft(**draft)

        pcd_create_draft_serialized = pcd_create_draft.serialize()

        assert pcd_create_draft_serialized["data"]["type"] == pcd_create_draft.type
        assert pcd_create_draft_serialized["data"]["attributes"]["name"] == pcd_create_draft.name


@pytest.mark.parametrize(
    "draft,exception",
    [
        (
            {
                "id": "id",
                "name": "Product package height in mm",
                "website_id": "website_id",
                "slot": 1,
            },
            does_not_raise(),
        ),
        (
            {
                "id": None,
                "name": "Product package height in mm",
                "website_id": "website_id",
                "slot": 1,
            },
            pytest.raises(ValidationError),
        ),
        (
            {
                "id": "id",
                "name": "Product package height in mm",
                "website_id": "website_id",
            },
            pytest.raises(ValidationError),
        ),
    ],
)
def test_serialize_pcd_update_draft(draft: dict[str, Any], exception):
    with exception:
        pcd_update_draft = ProductCustomDimensionUpdateDraft(**draft)

        pcd_update_draft_serialized = pcd_update_draft.serialize()

        assert pcd_update_draft_serialized["data"]["id"] == pcd_update_draft.id
        assert pcd_update_draft_serialized["data"]["type"] == pcd_update_draft.type
        assert pcd_update_draft_serialized["data"]["attributes"]["name"] == pcd_update_draft.name
