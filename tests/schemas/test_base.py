import datetime

import pytest

from pydantic import BaseModel

from piwik.schemas import base


class PageTestModel(BaseModel):
    id: str


@pytest.fixture
def page_of_test_models():
    return base.Page[PageTestModel].deserialize(
        {
            "meta": {"total": 1},
            "data": [{"id": "id"}],
        },
    )


@pytest.fixture
def base_schema():
    return base.BaseSchema.deserialize(
        {
            "type": "type",
            "id": "id",
            "addedAt": "2024-02-10",
            "updatedAt": "2024-02-10",
        },
    )


def test_page_deserialization(page_of_test_models: base.Page[PageTestModel]):
    assert page_of_test_models.page == 0
    assert page_of_test_models.size == 10
    assert page_of_test_models.total == 1
    assert len(page_of_test_models.data) == 1
    assert repr(page_of_test_models) == "Page<PageTestModel>(page=0, size=10, total=1)"


def test_page_serialization(page_of_test_models: base.Page[PageTestModel]):
    data = page_of_test_models.serialize()

    assert isinstance(data, dict)
    assert all(True if key in ["page", "size", "total", "data"] else False for key in data.keys())


def test_page_iteration(page_of_test_models: base.Page[PageTestModel]):
    for p in page_of_test_models:
        assert p.id == "id"

    for p in page_of_test_models.data:
        assert p.id == "id"


def test_page_getter(page_of_test_models: base.Page[PageTestModel]):
    assert page_of_test_models[0].id == "id"


def test_base_schema_deserialization(base_schema: base.BaseSchema):
    assert base_schema.id == "id"
    assert base_schema.type == "type"

    assert isinstance(base_schema.addedAt, datetime.date)
    assert isinstance(base_schema.updatedAt, datetime.date)


def test_base_schema_serialization(base_schema: base.BaseSchema):
    data = base_schema.serialize()

    assert isinstance(data, dict)
    assert all(True if key in ["id", "type", "addedAt", "updatedAt"] else False for key in data.keys())
