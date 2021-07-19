import os


class WebAppEventsConfig:
    HMAC_KEY = bytes.fromhex(os.environ['WEBAPP_EVENTS_HMAC_KEY'])

class WebAppConfig:
    events = WebAppEventsConfig()