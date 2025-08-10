import jwt
import time
import json
import uuid
from cryptography.hazmat.primitives.asymmetric import ed25519
import base64

print("🔧 GENERATING JWT WITH ED25519 SIGNATURE...")

# Load the raw private key
with open('ed25519_raw.key', 'r') as f:
    raw_key_b64 = f.read().strip()

# Create ED25519 private key from raw bytes
private_key_bytes = base64.b64decode(raw_key_b64)
private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)

# Coinbase API key ID
key_id = "2636c881-b44e-4263-b05d-fb10a5ad1836"

# Create JWT payload
timestamp = int(time.time())
nonce = str(uuid.uuid4()).replace('-', '')

payload = {
    "iss": "cdp",
    "nbf": timestamp,
    "exp": timestamp + 120,
    "sub": key_id,
    "uri": "GET /api/v3/brokerage/accounts"
}

# Create JWT with ED25519 signature
token = jwt.encode(
    payload,
    private_key,
    algorithm='EdDSA',
    headers={
        'kid': key_id,
        'nonce': nonce
    }
)

# Save JWT
with open('coinbase_jwt.txt', 'w') as f:
    f.write(token)

print(f"[✅] JWT generated and saved: coinbase_jwt.txt")
print(f"    Token length: {len(token)} chars")
print(f"    Expires: {timestamp + 120} ({time.ctime(timestamp + 120)})")
print(f"    Nonce: {nonce}")
