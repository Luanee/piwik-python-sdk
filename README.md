# Python SDK for Piwik

This is an unofficial Python REST API Wrapper for Piwik Pro. It only supports Python 3.8+ and uses type annotation for an improved development experience.

## Documentation

| Module         | API                        | Link                                                                                                                                                                  |
| -------------- | -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Administration | Apps                       | [Apps API](https://developers.piwik.pro/en/latest/platform/authorized_api/apps/apps_api.html)                                                                         |
|                | Meta Sites                 | [Meta Sites API](https://developers.piwik.pro/en/latest/platform/authorized_api/meta_sites/meta_sites_api.html)                                                       |
| Analytics      | Events                     | [Events API](https://developers.piwik.pro/en/latest/custom_reports/http_api/http_api.html#tag/Raw-data/paths/~1api~1analytics~1v1~1events~1/post)                     |
|                | Sessions                   | [Sessions API](https://developers.piwik.pro/en/latest/custom_reports/http_api/http_api.html#tag/Raw-data/paths/~1api~1analytics~1v1~1sessions~1/post)                 |
|                | Query                      | [Query API](https://developers.piwik.pro/en/latest/custom_reports/http_api/http_api.html#tag/Queries)                                                                 |
|                | Real-Time-Events           | [Real-Time-Events API](https://developers.piwik.pro/en/latest/custom_reports/http_api/http_api.html#tag/Raw-data/paths/~1api~1analytics~1v1~1real-time-events~1/post) |
|                | Goals                      | [Goals API](https://developers.piwik.pro/en/latest/custom_reports/object_management_api/object_management_api.html#tag/Goals)                                         |
|                | Custom Dimensions          | [Custom Dimensions API](https://developers.piwik.pro/en/latest/custom_reports/object_management_api/object_management_api.html#tag/Custom-Dimensions)                 |
|                | Product Custom Dimensions  | [Product Custom Dimensions API](https://developers.piwik.pro/en/latest/custom_reports/object_management_api/object_management_api.html#tag/Custom-Dimensions)         |
|                | System Annotations         | [System Annotations API](https://developers.piwik.pro/en/latest/custom_reports/object_management_api/object_management_api.html#tag/System-Annotations)               |
|                | User Annotations           | [User Annotations API](https://developers.piwik.pro/en/latest/custom_reports/object_management_api/object_management_api.html#tag/User-Annotations)                   |

## Installation

### Pip

```bash
pip install piwik-python-sdk
```

### Poetry

```bash
poetry add piwik-python-sdk
```

## Get started

### Initialize a Client directly

```python
client = Client(
    client_id="<client-id>",
    client_secret="<client-secret>",
    url="https://<account>.piwik.pro",
    auth_url="https://<account>.piwik.pro/auth/token",
)
```

The client can also be configured by setting the following environment variables:

```bash
export PIWIK_CLIENT_SECRET="<client secret>"
export PIWIK_CLIENT_ID="<client id>"
export PIWIK_URL="https://<account>.piwik.pro"
export PIWIK_AUTH_URL="https://<account>.piwik.pro/auth/token"
```

## Examples

### Search for specific apps

```python
from piwik import Client

client = Client()

page_of_apps = client.apps.list(search="DE", page=0, size=50)
print(page_of_apps)
```

More examples can be found here: [examples](./examples)
