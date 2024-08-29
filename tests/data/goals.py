from piwik.schemas.goals import GoalCreateDraft, GoalUpdateDraft

RESPONSE_DATA_GOAL = {
    "data": {
        "attributes": {
            "website_id": "website_id",
            "name": "User entered contact page",
            "description": "Goal is triggered when user enters contact page",
            "trigger": "url",
            "pattern_type": "contains",
            "pattern": "Contact",
            "allow_multiple": False,
            "case_sensitive": False,
            "revenue": "10.22",
        },
        "type": "Goal",
        "id": "id",
    }
}

GOAL_CREATE_DRAFT = GoalCreateDraft(
    name="User entered contact page",
    website_id="website_id",
    trigger="event_action",
    allow_multiple=True,
    case_sensitive=True,
    revenue=1,
)


GOAL_UPDATE_DRAFT = GoalUpdateDraft(
    id="cb093b59-045d-47eb-8c6e-0a7fbf15b14b",
    trigger="event_action",
    name="User entered contact page",
    website_id="website_id",
    revenue=1,
)
