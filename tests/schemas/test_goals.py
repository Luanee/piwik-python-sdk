from contextlib import nullcontext as does_not_raise
from typing import Any

import pytest
from pydantic import ValidationError

from piwik.schemas.goals import Goal, GoalCreateDraft, GoalUpdateDraft
from piwik.schemas.page import Page
from tests.data.goals import RESPONSE_DATA_GOAL
from tests.utils.helper import prepare_page_data


def test_deserialize_goal():
    goal = Goal.deserialize(RESPONSE_DATA_GOAL)
    assert goal.id == "id"
    assert goal.name == "User entered contact page"
    assert goal.website_id == "website_id"


def test_deserialize_goals_page():
    page_of_goals = Page[Goal].deserialize(
        prepare_page_data(RESPONSE_DATA_GOAL, 2),
        page=0,
        size=3,
    )
    assert page_of_goals.total == 2
    assert page_of_goals.page == 0
    assert page_of_goals.size == 3
    assert len(page_of_goals.data) == 2
    assert repr(page_of_goals) == "Page<Goal>(page=0, size=3, total=2)"

    page_of_goals = Page[Goal].deserialize(
        prepare_page_data(RESPONSE_DATA_GOAL, 0),
        page=0,
        size=3,
    )
    assert page_of_goals.total == 0
    assert page_of_goals.page == 0
    assert page_of_goals.size == 3
    assert len(page_of_goals.data) == 0
    assert repr(page_of_goals) == "Page<Goal>(page=0, size=3, total=0)"


@pytest.mark.parametrize(
    "draft,exception",
    [
        (
            {
                "name": "User entered contact page",
                "website_id": "website_id",
                "trigger": "event_action",
                "allow_multiple": True,
                "case_sensitive": True,
                "revenue": 1,
            },
            does_not_raise(),
        ),
        (
            {
                "name": "User entered contact page",
                "website_id": "website_id",
                "trigger": "event_action",
                "allow_multiple": True,
                "case_sensitive": True,
                "revenue": "hello",
            },
            pytest.raises(ValidationError),
        ),
        (
            {
                "name": "User entered contact page",
                "website_id": "website_id",
                "trigger": "dump",
                "allow_multiple": True,
                "case_sensitive": True,
                "revenue": 1,
            },
            pytest.raises(ValidationError),
        ),
    ],
)
def test_serialize_goal_create_draft(draft: dict[str, Any], exception):
    with exception:
        goal_create_draft = GoalCreateDraft(**draft)

        goal_create_draft_serialized = goal_create_draft.serialize()

        assert goal_create_draft_serialized["data"]["type"] == goal_create_draft.type
        assert goal_create_draft_serialized["data"]["attributes"]["name"] == goal_create_draft.name
        assert goal_create_draft_serialized["data"]["attributes"]["case_sensitive"] == goal_create_draft.case_sensitive


@pytest.mark.parametrize(
    "draft,exception",
    [
        (
            {
                "id": "id",
                "name": "User entered contact page",
                "website_id": "website_id",
                "trigger": "event_action",
                "revenue": 1,
            },
            does_not_raise(),
        ),
        (
            {
                "id": "id",
                "name": "User entered contact page",
                "website_id": "website_id",
                "trigger": "event_action",
            },
            pytest.raises(ValidationError),
        ),
        (
            {
                "id": "id",
                "name": "User entered contact page",
                "website_id": "website_id",
                "trigger": "dump",
                "revenue": 1,
            },
            pytest.raises(ValidationError),
        ),
        (
            {
                "id": None,
                "name": "User entered contact page",
                "website_id": "website_id",
                "trigger": "event_action",
                "revenue": 1,
            },
            pytest.raises(ValidationError),
        ),
    ],
)
def test_serialize_goal_update_draft(draft: dict[str, Any], exception):
    with exception as e:
        goal_update_draft = GoalUpdateDraft(**draft)

        goal_update_draft_serialized = goal_update_draft.serialize()

        assert goal_update_draft_serialized["data"]["id"] == goal_update_draft.id
        assert goal_update_draft_serialized["data"]["type"] == goal_update_draft.type
        assert goal_update_draft_serialized["data"]["attributes"]["name"] == goal_update_draft.name
        assert "case_sensitive" not in goal_update_draft_serialized["data"]["attributes"]
