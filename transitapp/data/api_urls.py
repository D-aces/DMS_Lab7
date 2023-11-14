import environ

# Initialise environment variables
env = environ.Env()
environ.Env.read_env()

api_urls = [
    'https://dataportal.greatersudbury.ca/api/v2/routes?auth_token=' + env('MyBusAPI_AUTH_TOKEN'),
    'https://dataportal.greatersudbury.ca/api/v2/stops?auth_token=' + env('MyBusAPI_AUTH_TOKEN'),
    'https://dataportal.greatersudbury.ca/api/v2/destinations?auth_token=' + env('MyBusAPI_AUTH_TOKEN'),
    'https://dataportal.greatersudbury.ca/api/v2/destinations/',
    'https://dataportal.greatersudbury.ca/api/v2/stops/'
]