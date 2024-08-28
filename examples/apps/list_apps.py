from piwik import Client


client = Client()

# returns all apps
page_of_apps = client.administration.apps.list()

# returns all apps that contains 'DE'
page_of_apps = client.administration.apps.list(search="DE")

# returns all apps (depending on the size) but will skip the first 20 apps
page_of_apps = client.administration.apps.list(page=10, size=2)

# output all apps
for app in page_of_apps:
    print(app)

# or:
for app in page_of_apps.data:
    print(app)
