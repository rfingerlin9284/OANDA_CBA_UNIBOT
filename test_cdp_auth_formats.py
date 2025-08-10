#!/usr/bin/env python3
"""
🔧 COINBASE CDP API AUTHENTICATION TEST
Test with proper CDP API format
"""

import requests
import jwt
import time
import uuid
import base64
from cryptography.hazmat.primitives.asymmetric import ed25519

def test_cdp_auth():
    """Test Coinbase Developer Platform API authentication"""
    print("🔧 TESTING COINBASE CDP API AUTHENTICATION...")
    
    # Your credentials from the JSON
    api_key = "2636c881-b44e-4263-b05d-fb10a5ad1836"
    private_key_b64 = "s+jUeS54GxpxQ3WOM5uLHHlm9JhCIrtBeE9X1Drn2IfPHg6yie2q+GEAIwRJGkAkZyUOgY0YQE27H1R5CNFGGg=="
    
    # Decode the private key (take first 32 bytes if 64)
    private_key_bytes = base64.b64decode(private_key_b64)
    if len(private_key_bytes) == 64:
        private_key_bytes = private_key_bytes[:32]
    
    print(f"Private key length: {len(private_key_bytes)} bytes")
    
    # Create ED25519 private key
    private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_key_bytes)
    
    # Try different endpoints
    endpoints_to_test = [
        ("https://api.coinbase.com/api/v3/brokerage/accounts", "Coinbase Advanced Trade"),
        ("https://api.cdp.coinbase.com/platform/accounts", "CDP Platform"),
        ("https://api.coinbase.com/v2/accounts", "Coinbase API v2"),
    ]
    
    for url, name in endpoints_to_test:
        print(f"\n🧪 Testing {name}: {url}")
        
        # Generate JWT
        timestamp = int(time.time())
        nonce = str(uuid.uuid4()).replace('-', '')
        
        # Determine the path from URL
        if "v3/brokerage" in url:
            path = "/api/v3/brokerage/accounts"
        elif "platform" in url:
            path = "/platform/accounts"
        elif "v2" in url:
            path = "/v2/accounts"
        else:
            path = "/accounts"
        
        payload = {
            "iss": "cdp",
            "nbf": timestamp,
            "exp": timestamp + 120,
            "sub": api_key,
            "uri": f"GET {path}"
        }
        
        token = jwt.encode(
            payload,
            private_key,
            algorithm='EdDSA',
            headers={'kid': api_key, 'nonce': nonce}
        )
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "WolfpackLite/1.0"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"    Response: {response.status_code}")
            
            if response.status_code == 200:
                print(f"    ✅ Success! {name} working")
                data = response.json()
                print(f"    Data keys: {list(data.keys()) if isinstance(data, dict) else 'Not dict'}")
            elif response.status_code == 401:
                print(f"    ❌ 401 Unauthorized - {name}")
            elif response.status_code == 403:
                print(f"    ❌ 403 Forbidden - {name}")
            elif response.status_code == 404:
                print(f"    ⚠️ 404 Not Found - Wrong endpoint")
            else:
                print(f"    ⚠️ {response.status_code} - {response.text[:100]}")
                
        except requests.exceptions.RequestException as e:
            print(f"    ❌ Request failed: {e}")
    
    # Test with different JWT formats
    print(f"\n🔧 TESTING DIFFERENT JWT FORMATS...")
    
    # Format 1: Standard CDP
    payload1 = {
        "iss": "cdp",
        "nbf": timestamp,
        "exp": timestamp + 120,
        "sub": api_key,
        "uri": "GET /api/v3/brokerage/accounts"
    }
    
    # Format 2: Minimal
    payload2 = {
        "iss": "coinbase-cloud",
        "sub": api_key,
        "exp": timestamp + 120,
    }
    
    # Format 3: Alternative
    payload3 = {
        "iss": "cdp",
        "sub": api_key,
        "aud": ["retail_rest_api_proxy"],
        "nbf": timestamp,
        "exp": timestamp + 120,
        "uri": "GET /api/v3/brokerage/accounts"
    }
    
    payloads = [
        (payload1, "Standard CDP"),
        (payload2, "Minimal"),
        (payload3, "Alternative")
    ]
    
    for payload, desc in payloads:
        print(f"\n  Testing {desc} format...")
        
        token = jwt.encode(
            payload,
            private_key,
            algorithm='EdDSA',
            headers={'kid': api_key, 'nonce': str(uuid.uuid4()).replace('-', '')}
        )
        
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get("https://api.coinbase.com/api/v3/brokerage/accounts", 
                                  headers=headers, timeout=5)
            print(f"    {desc}: {response.status_code}")
            if response.status_code != 401:
                print(f"    Response: {response.text[:200]}")
        except Exception as e:
            print(f"    {desc}: Error - {e}")

if __name__ == "__main__":
    test_cdp_auth()
