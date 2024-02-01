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

### Initialize a Client via environment variables

Setup your environments with these variables:

```sh
export PIWIK_URL="https://<account>.piwik.pro"
export PIWIK_AUTH_URL="https://<account>.piwik.pro/auth/token"
export PIWIK_CLIENT_ID="<client-id>"
export PIWIK_CLIENT_SECRET="<client-secret>"
```

```python
client = Client()
```

## Examples

### Search for specific apps

```python
from piwik import Client

client = Client()

page_of_apps = client.apps.list(search="DE", page=0, size=50)
print(page_of_apps)
```
