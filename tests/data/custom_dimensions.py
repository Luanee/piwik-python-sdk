from piwik.schemas.custom_dimensions import CustomDimensionCreateDraft, CustomDimensionUpdateDraft, Extraction

RESPONSE_DATA_CUSTOM_DIMENSION = {
    "data": {
        "type": "CustomDimension",
        "id": "id",
        "attributes": {
            "website_id": "website_id",
            "name": "Visitor hair color",
            "active": True,
            "case_sensitive": True,
            "tracking_id": 1,
            "extractions": [{"target": "page_title_regex", "pattern": "/foo/(.*)/bar"}],
            "scope": "session",
            "slot": 1,
        },
    }
}

CUSTOM_DIMENSION_CREATE_DRAFT = CustomDimensionCreateDraft(
    name="Visitor hair color",
    website_id="website_id",
    active=True,
    slot=1,
    scope="event",
    extractions=[
        Extraction(target="page_title_regex", pattern="/foo/(.*)/bar"),
    ],
    case_sensitive=True,
)


CUSTOM_DIMENSION_UPDATE_DRAFT = CustomDimensionUpdateDraft(
    id="id",
    name="Visitor hair color",
    website_id="website_id",
    active=True,
    scope="event",
    extractions=[
        Extraction(target="page_title_regex", pattern="/foo/(.*)/bar"),
    ],
    case_sensitive=True,
)
