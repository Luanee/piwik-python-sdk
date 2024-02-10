"""
Demonstrates how to authenticate with client credentials (id and secret)

Refer this article for a detailed instruction:
https://developers.piwik.pro/en/latest/platform/getting_started.html#
"""

from piwik.client import Client


# Initialize a Client via necessary auth parameter
client = Client(
    client_id="<client-id>",
    client_secret="<client-secret>",
    url="https://<account>.piwik.pro",
    auth_url="https://<account>.piwik.pro/auth/token",
)


# Initialize a Client via environment variables
# Make sure that following environment variables are ready to use
# PIWIK_URL             - host of piwik instance
# PIWIK_AUTH_URL        - auth host of piwik instances
# PIWIK_CLIENT_ID       - id of generated api credentials
# PIWIK_CLIENT_SECRET   - secret of generated api credentials
client = Client()
