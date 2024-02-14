from piwik.schemas.apps import AppCreateDraft, AppUpdateDraft


RESPONSE_DATA_APP = {
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

RESPONSE_DATA_BASE_APP = {
    "type": "ppms/app",
    "id": f"cb093b59-045d-47eb-8c6e-0a7fbf15b11b",
    "attributes": {
        "name": f"Demo site 1",
        "addedAt": "2024-02-07T20:03:33+00:00",
        "updatedAt": "2024-02-07T20:03:33+00:00",
    },
}

RESPONSE_DATA_PERMISSION_BASE = {
    "type": "ppms/app_permission_for_user_group",
    "id": "944c3164-31d5-4c2e-80de-d9ae527c4780",
    "attributes": {
        "app_name": "Demo site",
        "access": "no-access",
    },
}

APP_CREATE_DRAFT = AppCreateDraft(name="Demo site", urls=["https://demo.org"])
APP_UPDATE_DRAFT = AppUpdateDraft(id="cb093b59-045d-47eb-8c6e-0a7fbf15b14b", currency="USD")
