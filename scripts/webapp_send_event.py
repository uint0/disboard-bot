import os
import sys
import hmac
import hashlib

import requests


hmac_key = bytes.fromhex(os.environ['WEBAPP_EVENTS_HMAC_KEY'])

path, payload = sys.argv[1:]

resp = requests.post(
    f"http://localhost:8000/events/{path.lstrip('/')}",
    data=payload,
    headers={
        'Content-Type': 'application/json',
        'X-Event-Payload-HMAC': hmac.digest(hmac_key, payload.encode(), hashlib.sha256).hex()
    }
)

print(resp)
print(resp.text)
