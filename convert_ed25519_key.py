#!/usr/bin/env python3
"""
🔧 ED25519 Key Format Converter
Convert PEM format to the correct base64 format for Coinbase API
"""

import base64
from cryptography.hazmat.primitives import serialization

def convert_pem_to_raw_base64(pem_key):
    """Convert PEM private key to raw 32-byte base64 format"""
    try:
        # Load the PEM private key
        private_key_obj = serialization.load_pem_private_key(
            pem_key.encode('utf-8'),
            password=None
        )
        
        # Extract raw private bytes (32 bytes for ED25519)
        raw_private_bytes = private_key_obj.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Convert to base64
        b64_private_key = base64.b64encode(raw_private_bytes).decode('utf-8')
        
        return b64_private_key, len(raw_private_bytes)
        
    except Exception as e:
        return None, str(e)

def main():
    # Your current PEM key
    pem_key = """-----BEGIN PRIVATE KEY-----
MC4CAQAwBQYDK2VwBCIEILPo1HkueBsacUN1jjObixx5ZvSYQiK7QXhPV9Q659iH
-----END PRIVATE KEY-----"""
    
    print("🔧 ED25519 Key Format Converter")
    print("=" * 40)
    
    print("📋 Input PEM Key:")
    print(pem_key)
    print()
    
    b64_key, length = convert_pem_to_raw_base64(pem_key)
    
    if b64_key:
        print("✅ Conversion Successful!")
        print(f"📏 Raw key length: {length} bytes")
        print(f"🔑 Base64 private key: {b64_key}")
        print()
        print("💡 Use this value for COINBASE_PRIVATE_KEY_B64:")
        print(f'COINBASE_PRIVATE_KEY_B64 = "{b64_key}"')
    else:
        print(f"❌ Conversion failed: {length}")

if __name__ == "__main__":
    main()
