#!/usr/bin/env python3
"""
Generate Coinbase Advanced HMAC signature (base64) for testing.
Usage: python3 coinbase_sign_hmac.py method path body timestamp
"""
import os, sys, hmac, hashlib, base64
api_secret = os.getenv('CB_API_SECRET')
if len(sys.argv) != 5:
    print("Usage: sign_hmac.py METHOD PATH BODY TIMESTAMP", file=sys.stderr)
    sys.exit(1)
method, path, body, timestamp = sys.argv[1:]
message = timestamp + method.upper() + path + body
secret = base64.b64decode(api_secret)
signature = hmac.new(secret, message.encode(), hashlib.sha256).digest()
print(base64.b64encode(signature).decode())
