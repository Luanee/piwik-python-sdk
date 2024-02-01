# Python SDK for Piwik

This is an unofficial Python SDK for piwik pro.

## Installation

### Pip

```bash
pip install piwik-python-sdk
```

### Poetry

```bash
poetry add piwik-python-sdk
```

## Examples

```python
from piwik import Client

client = Client(
    client_id="<your-client-id>",
    client_secret="<your-client-secret>",
    url="https://<account>.piwik.pro",
    auth_url="https://<account>.piwik.pro/auth/token",
)

page_of_apps = client.apps.list()
print(page_of_apps)
```
