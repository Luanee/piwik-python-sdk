# Python SDK for Piwik

This is an unofficial Python REST API Wrapper for Piwik Pro.

## DOcumentation

| Module         | API         | Link                                                                                                            |
| -------------- | ----------- | --------------------------------------------------------------------------------------------------------------- |
| Administration | Apps        | [Apps API](https://developers.piwik.pro/en/latest/platform/authorized_api/apps/apps_api.html)                   |
|                | Meta Sites  | [Meta Sites API](https://developers.piwik.pro/en/latest/platform/authorized_api/meta_sites/meta_sites_api.html) |

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

## Examples

### Search for specific apps

```python
from piwik import Client

client = Client()

page_of_apps = client.apps.list(search="DE", page=0, size=50)
print(page_of_apps)
```

More examples can be found here: [examples](./examples)
