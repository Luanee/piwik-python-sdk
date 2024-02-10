from piwik import Client
from piwik.schemas.apps import App


client = Client()

ID = "<app-id>"

app: App | None = client.apps.get(id=ID)
print(app)
