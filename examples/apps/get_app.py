from piwik import Client
from piwik.schemas.apps import App


client = Client()

ID = "<app-id>"

app: App | None = client.administration.apps.get(id=ID)
print(app)
