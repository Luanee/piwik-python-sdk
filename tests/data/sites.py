from piwik.schemas.sites import SiteCreateDraft, SiteUpdateDraft


RESPONSE_DATA_SITE = {
    "data": {
        "id": "6edb1e3c-4c43-4760-ab76-682ad83146be",
        "type": "ppms/meta-site",
        "attributes": {
            "name": "All apps",
            "currency": "USD",
            "timezone": "Europe/Warsaw",
            "e_commerce_tracking": False,
            "sharepoint_integration": False,
            "cnil": False,
            "created_at": "2024-02-24T14:59:47Z",
            "updated_at": "2024-02-24T14:59:47Z",
            "organization": "default",
        },
    }
}

RESPONSE_DATA_BASE_SITE = {
    "type": "ppms/meta-site",
    "id": f"cb093b59-045d-47eb-8c6e-0a7fbf15b11b",
    "attributes": {
        "name": f"Demo site 1",
        "addedAt": "2024-02-07T20:03:33+00:00",
        "updatedAt": "2024-02-07T20:03:33+00:00",
    },
}

RESPONSE_DATA_META_SITE_APP = {
    "type": "ppms/app",
    "id": f"cb093b59-045d-47eb-8c6e-0a7fbf15b11b",
    "attributes": {
        "name": f"Demo site 1",
        "addedAt": "2024-02-07T20:03:33+00:00",
        "updatedAt": "2024-02-07T20:03:33+00:00",
        "currency": "USD",
        "timezone": "Europe/Warsaw",
        "cnil": False,
    },
}

RESPONSE_DATA_SITE_INTEGRITY_BASE = {
    "type": "meta-site/apps/integrity",
    "id": "944c3164-31d5-4c2e-80de-d9ae527c4780",
    "attributes": {
        "valid_currency": True,
        "valid_timezone": False,
    },
}

SITE_CREATE_DRAFT = SiteCreateDraft(name="Demo site")
SITE_UPDATE_DRAFT = SiteUpdateDraft(id="cb093b59-045d-47eb-8c6e-0a7fbf15b14b", currency="USD")
