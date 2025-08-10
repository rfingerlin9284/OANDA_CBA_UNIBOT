#!/usr/bin/env python3
"""
Debug script to determine proper Ed25519 key format and generate PEM
"""

import os
import base64
import logging
from dotenv import load_dotenv
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

load_dotenv()

def debug_key_format():
    """Debug the private key format and find working solution"""
    
    private_key_b64 = os.getenv("COINBASE_API_PRIVATE_KEY")
    api_key_id = os.getenv("COINBASE_API_KEY_ID")
    
    print(f"API Key ID: {api_key_id}")
    print(f"Private Key: {private_key_b64}")
    print(f"Key Length: {len(private_key_b64)}")
    print(f"Length % 4: {len(private_key_b64) % 4}")
    print()
    
    # Try different approaches to fix the base64 key
    approaches = [
        ("Direct decode", lambda k: base64.b64decode(k)),
        ("Remove last char", lambda k: base64.b64decode(k[:-1])),
        ("Add padding", lambda k: base64.b64decode(k + "=")),
        ("Add double padding", lambda k: base64.b64decode(k + "==")),
        ("Add triple padding", lambda k: base64.b64decode(k + "===")),
        ("URL safe decode", lambda k: base64.urlsafe_b64decode(k + "==")),
    ]
    
    working_key = None
    working_method = None
    
    for method_name, decode_func in approaches:
        try:
            decoded_bytes = decode_func(private_key_b64)
            print(f"{method_name}: Decoded {len(decoded_bytes)} bytes")
            
            # Try different byte positions for 32-byte ed25519 seed
            for offset in [0, 32, len(decoded_bytes) - 32] if len(decoded_bytes) >= 32 else [0]:
                try:
                    if offset + 32 <= len(decoded_bytes):
                        seed = decoded_bytes[offset:offset + 32]
                        key = ed25519.Ed25519PrivateKey.from_private_bytes(seed)
                        
                        # Generate PEM format
                        pem = key.private_bytes(
                            encoding=serialization.Encoding.PEM,
                            format=serialization.PrivateFormat.PKCS8,
                            encryption_algorithm=serialization.NoEncryption()
                        )
                        
                        print(f"✓ SUCCESS: {method_name} with offset {offset}")
                        print(f"  Seed length: {len(seed)} bytes")
                        print(f"  PEM format generated successfully")
                        print(f"  PEM Preview: {pem.decode()[:100]}...")
                        
                        working_key = seed
                        working_method = method_name
                        working_pem = pem.decode()
                        
                        # Test JWT generation
                        import jwt
                        import time
                        
                        payload = {
                            "iat": int(time.time()),
                            "exp": int(time.time()) + 60,
                            "iss": api_key_id,
                            "sub": api_key_id,
                            "request": {
                                "path": "/api/v3/brokerage/accounts",
                                "method": "GET",
                                "body": ""
                            }
                        }
                        
                        jwt_token = jwt.encode(payload, pem, algorithm="EdDSA")
                        print(f"  JWT Token: {jwt_token[:50]}...")
                        
                        return {
                            "method": method_name,
                            "offset": offset,
                            "seed_hex": seed.hex(),
                            "seed_b64": base64.b64encode(seed).decode(),
                            "pem": working_pem,
                            "jwt_sample": jwt_token
                        }
                        
                except Exception as e:
                    print(f"  Failed at offset {offset}: {e}")
                    
        except Exception as e:
            print(f"{method_name}: Failed - {e}")
        
        print()
    
    print("❌ No working method found")
    return None

if __name__ == "__main__":
    result = debug_key_format()
    
    if result:
        print("\n" + "="*60)
        print("WORKING SOLUTION FOUND:")
        print("="*60)
        print(f"Method: {result['method']}")
        print(f"Offset: {result['offset']}")
        print(f"Seed (hex): {result['seed_hex']}")
        print(f"Seed (base64): {result['seed_b64']}")
        print(f"PEM Format:\n{result['pem']}")
        print("\n.env Addition:")
        print(f"COINBASE_API_PRIVATE_KEY_SEED={result['seed_b64']}")
        print(f"COINBASE_API_PRIVATE_KEY_PEM_START=-----BEGIN PRIVATE KEY-----")
        print(f"COINBASE_API_PRIVATE_KEY_PEM_END=-----END PRIVATE KEY-----")
    else:
        print("\n❌ Could not determine working key format")
