"""
Build a short-lived JWT for Coinbase (optional flow).
Requires: pip install pyjwt cryptography
.env values used:
  COINBASE_JWT_ISS, COINBASE_JWT_AUD, COINBASE_JWT_TTL_SEC, COINBASE_API_KEY (as sub)
  CB_ED25519_PRIVATE_KEY_PEM_PATH
"""
import os, time, json
import jwt  # pyjwt
from datetime import datetime, timezone, timedelta
from cryptography.hazmat.primitives import serialization

iss = os.getenv("COINBASE_JWT_ISS","unibot")
aud = os.getenv("COINBASE_JWT_AUD","retail_rest_api")
sub = os.getenv("COINBASE_API_KEY","")
ttl = int(os.getenv("COINBASE_JWT_TTL_SEC","30"))
pem_path = os.getenv("CB_ED25519_PRIVATE_KEY_PEM_PATH","config/keys/cb_ed25519_private.pem")

if not sub:
  raise SystemExit("COINBASE_API_KEY (sub) missing")
with open(pem_path,"rb") as f:
  key = serialization.load_pem_private_key(f.read(), password=None)

now = datetime.now(timezone.utc)
payload = {
  "iss": iss,
  "sub": sub,
  "aud": aud,
  "iat": int(now.timestamp()),
  "exp": int((now + timedelta(seconds=ttl)).timestamp()),
}
token = jwt.encode(payload, key, algorithm="EdDSA", headers={"typ":"JWT"})
print(token)
