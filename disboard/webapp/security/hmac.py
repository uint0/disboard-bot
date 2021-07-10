import hmac
import hashlib

import config

def ensure_request_integrity(request_body: bytes, request_hash: str):
    sent_hmac = bytes.fromhex(request_hash)
    calced_hmac = hmac.digest(
        config.webapp.events.HMAC_KEY,
        request_body,
        hashlib.sha256
    )

    return hmac.compare_digest(sent_hmac, calced_hmac)


