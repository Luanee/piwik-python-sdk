from contextlib import nullcontext as does_not_raise
from typing import Any

import pytest

from pydantic import ValidationError

from piwik.schemas import apps


def test_deserialize_app():
    app = apps.App.deserialize(
        {
            "data": {
                "type": "ppms/app",
                "id": "cb093b59-045d-47eb-8c6e-0a7fbf15b14b",
                "attributes": {
                    "name": "Demo site",
                    "addedAt": "2024-02-07T20:03:33+00:00",
                    "updatedAt": "2024-02-07T22:40:02+00:00",
                    "urls": ["https://demo.org"],
                    "timezone": "UTC",
                    "currency": "USD",
                    "excludeUnknownUrls": False,
                    "keepUrlFragment": True,
                    "eCommerceTracking": True,
                    "siteSearchTracking": True,
                    "siteSearchQueryParams": ["q", "query", "s", "search", "searchword", "keyword"],
                    "siteSearchCategoryParams": [],
                    "delay": 500,
                    "excludedIps": [],
                    "excludedUrlParams": [
                        "gclid",
                        "fbclid",
                        "fb_xd_fragment",
                        "fb_comment_id",
                        "phpsessid",
                        "jsessionid",
                        "sessionid",
                        "aspsessionid",
                        "doing_wp_cron",
                        "sid",
                        "pk_vid",
                    ],
                    "excludedUserAgents": [],
                    "gdpr": True,
                    "gdprUserModeEnabled": False,
                    "privacyCookieDomainsEnabled": False,
                    "privacyCookieExpirationPeriod": 31536000,
                    "privacyCookieDomains": [],
                    "organization": "demo",
                    "appType": "web",
                    "gdprLocationRecognition": True,
                    "gdprDataAnonymization": True,
                    "sharepointIntegration": False,
                    "gdprDataAnonymizationMode": "session_cookie_id",
                    "privacyUseCookies": True,
                    "privacyUseFingerprinting": True,
                    "cnil": False,
                    "sessionIdStrictPrivacyMode": False,
                },
            }
        }
    )
    assert app.id == "cb093b59-045d-47eb-8c6e-0a7fbf15b14b"
    assert app.name == "Demo site"
    assert app.currency == "USD"


def test_deserialize_apps_page():
    page_of_apps = apps.AppsPage.deserialize(
        {
            "meta": {"total": 2},
            "data": [
                {
                    "type": "ppms/app",
                    "id": "cb093b59-045d-47eb-8c6e-0a7fbf15b14b",
                    "attributes": {
                        "name": "Demo site",
                        "addedAt": "2024-02-07T20:03:33+00:00",
                        "updatedAt": "2024-02-07T20:03:33+00:00",
                    },
                },
                {
                    "type": "ppms/app",
                    "id": "cb093b59-045d-47eb-8c6e-0a7fbf15b14c",
                    "attributes": {
                        "name": "Demo site 2",
                        "addedAt": "2024-02-07T20:03:33+00:00",
                        "updatedAt": "2024-02-07T22:40:02+00:00",
                    },
                },
            ],
        },
        page=0,
        size=3,
    )
    assert page_of_apps.total == 2
    assert page_of_apps.page == 0
    assert page_of_apps.size == 3
    assert len(page_of_apps.data) == 2
    assert repr(page_of_apps) == "Page<BaseApp>(page=0, size=3, total=2)"

    page_of_apps = apps.AppsPage.deserialize(
        {
            "meta": {"total": 0},
            "data": [],
        },
        page=0,
        size=3,
    )
    assert page_of_apps.total == 0
    assert page_of_apps.page == 0
    assert page_of_apps.size == 3
    assert len(page_of_apps.data) == 0
    assert repr(page_of_apps) == "Page<BaseApp>(page=0, size=3, total=0)"


@pytest.mark.parametrize(
    "draft,exception",
    [
        ({"name": "Demo Site 3", "urls": ["https://demosite3.com"]}, does_not_raise()),
        ({"name": "Demo Site 3", "urls": ["demosite3.com"]}, pytest.raises(ValidationError)),
        ({"name": "Demo Site 3", "urls": ["https://demosite3.com"], "type": "apps"}, pytest.raises(ValidationError)),
    ],
)
def test_serialize_app_create_draft(draft: dict[str, Any], exception):
    with exception as e:
        app_create_draft = apps.AppCreateDraft(**draft)

        app_create_draft_serialized = app_create_draft.serialize()

        assert app_create_draft_serialized["data"]["type"] == app_create_draft.type
        assert app_create_draft_serialized["data"]["attributes"]["name"] == app_create_draft.name
        assert app_create_draft_serialized["data"]["attributes"]["urls"] == app_create_draft.urls


@pytest.mark.parametrize(
    "draft,exception",
    [
        ({"id": "id", "name": "Demo Site 3", "urls": ["https://demosite3.com"]}, does_not_raise()),
        ({"id": "id", "name": "Demo Site 3", "urls": ["demosite3.com"]}, pytest.raises(ValidationError)),
        (
            {"id": "id", "name": "Demo Site 3", "urls": ["https://demosite3.com"], "type": "apps"},
            pytest.raises(ValidationError),
        ),
    ],
)
def test_serialize_app_update_draft(draft: dict[str, Any], exception):
    with exception as e:
        app_update_draft = apps.AppUpdateDraft(**draft)

        app_update_draft_serialized = app_update_draft.serialize()

        assert app_update_draft_serialized["data"]["id"] == app_update_draft.id
        assert app_update_draft_serialized["data"]["type"] == app_update_draft.type
        assert app_update_draft_serialized["data"]["attributes"]["name"] == app_update_draft.name
        assert app_update_draft_serialized["data"]["attributes"]["urls"] == app_update_draft.urls
