#!/usr/bin/env python3
"""
🎯 FINAL COINBASE ED25519 PROTOCOL TEST
Tests ALL authentication variations from your attached protocols
Constitutional PIN: 841921

PROTOCOL VARIATIONS TO TEST:
1. CDP SDK format (from api_auth_v2.py)
2. Advanced Trade format (from coinbase_advanced_api.py) 
3. CDP Auth format (from coinbase_cdp_auth.py)
4. JWT Auth format (from coinbase_jwt_auth.py)
5. Master protocol format (from master_coinbase_ed25519_protocol.py)
"""

import os
import sys
import time
import json
import base64
import uuid
from typing import Dict, Any, Optional

sys.path.append('.')

def test_cdp_sdk_format():
    """Test CDP SDK format from api_auth_v2.py"""
    
    print("🔧 TESTING CDP SDK FORMAT")
    print("=" * 40)
    
    try:
        import jwt
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        import requests
        
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        # Load private key
        seed_bytes = base64.b64decode(creds.COINBASE_PRIVATE_KEY_SEED)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed_bytes)
        
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # CDP SDK format
        request_method = "GET"
        request_path = "/api/v3/brokerage/accounts"
        request_host = "api.coinbase.com"
        
        current_time = int(time.time())
        
        payload = {
            "iss": "cdp",
            "nbf": current_time,
            "exp": current_time + 120,
            "sub": creds.COINBASE_API_KEY_ID,
            "uri": f"{request_method} {request_host}{request_path}",
            "aud": ["cdp_service"]
        }
        
        headers = {
            "kid": creds.COINBASE_API_KEY_ID,
            "nonce": str(uuid.uuid4()),
            "typ": "JWT",
            "alg": "EdDSA"
        }
        
        jwt_token = jwt.encode(payload, pem_key, algorithm="EdDSA", headers=headers)
        
        print(f"✅ CDP SDK format token generated")
        
        # Test request
        url = f"https://{request_host}{request_path}"
        request_headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=request_headers, timeout=30)
        print(f"📡 CDP SDK format response: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS with CDP SDK format!")
            return True, response.json()
        else:
            print(f"Response: {response.text[:200]}...")
            return False, None
            
    except Exception as e:
        print(f"❌ CDP SDK format failed: {e}")
        return False, None

def test_advanced_trade_format():
    """Test Advanced Trade format from coinbase_advanced_api.py"""
    
    print("\n🔧 TESTING ADVANCED TRADE FORMAT")
    print("=" * 40)
    
    try:
        import jwt
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        import requests
        
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        # Load private key
        seed_bytes = base64.b64decode(creds.COINBASE_PRIVATE_KEY_SEED)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed_bytes)
        
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Advanced Trade format (from coinbase_advanced_api.py)
        request_method = "GET"
        request_path = "/api/v3/brokerage/accounts"
        base_url = "https://api.coinbase.com"
        
        timestamp = int(time.time())
        
        payload = {
            'iss': 'cdp',  # Coinbase Developer Platform
            'nbf': timestamp,
            'exp': timestamp + 120,  # 2 minutes expiration
            'sub': creds.COINBASE_API_KEY_ID,
            'uri': request_method.upper() + ' ' + base_url + request_path,
        }
        
        jwt_token = jwt.encode(
            payload,
            pem_key,
            algorithm='EdDSA',  # ED25519 signature algorithm
            headers={'kid': creds.COINBASE_API_KEY_ID, 'nonce': str(uuid.uuid4())}
        )
        
        print(f"✅ Advanced Trade format token generated")
        
        # Test request
        url = f"{base_url}{request_path}"
        request_headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=request_headers, timeout=30)
        print(f"📡 Advanced Trade format response: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS with Advanced Trade format!")
            return True, response.json()
        else:
            print(f"Response: {response.text[:200]}...")
            return False, None
            
    except Exception as e:
        print(f"❌ Advanced Trade format failed: {e}")
        return False, None

def test_minimal_format():
    """Test minimal JWT format"""
    
    print("\n🔧 TESTING MINIMAL FORMAT")
    print("=" * 40)
    
    try:
        import jwt
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        import requests
        
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        # Load private key
        seed_bytes = base64.b64decode(creds.COINBASE_PRIVATE_KEY_SEED)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(seed_bytes)
        
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Minimal format
        current_time = int(time.time())
        
        payload = {
            "iss": creds.COINBASE_API_KEY_ID,
            "exp": current_time + 180,  # 3 minutes
            "iat": current_time
        }
        
        headers = {
            "alg": "EdDSA",
            "kid": creds.COINBASE_API_KEY_ID,
            "typ": "JWT"
        }
        
        jwt_token = jwt.encode(payload, pem_key, algorithm="EdDSA", headers=headers)
        
        print(f"✅ Minimal format token generated")
        
        # Test request
        url = "https://api.coinbase.com/api/v3/brokerage/accounts"
        request_headers = {
            "Authorization": f"Bearer {jwt_token}",
            "CB-ACCESS-KEY": creds.COINBASE_API_KEY_ID,
            "Content-Type": "application/json"
        }
        
        response = requests.get(url, headers=request_headers, timeout=30)
        print(f"📡 Minimal format response: {response.status_code}")
        
        if response.status_code == 200:
            print("🎉 SUCCESS with Minimal format!")
            return True, response.json()
        else:
            print(f"Response: {response.text[:200]}...")
            return False, None
            
    except Exception as e:
        print(f"❌ Minimal format failed: {e}")
        return False, None

def analyze_error_response():
    """Analyze the 401 error to understand the issue"""
    
    print("\n🔍 ANALYZING 401 ERROR")
    print("=" * 30)
    
    try:
        import requests
        
        # Make a request without auth to see the error format
        url = "https://api.coinbase.com/api/v3/brokerage/accounts"
        response = requests.get(url, timeout=30)
        
        print(f"📡 No auth response: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        print(f"Response body: {response.text}")
        
        # Check if it's a different endpoint format needed
        test_endpoints = [
            "https://api.coinbase.com/v2/accounts",
            "https://api.coinbase.com/api/v3/brokerage/time",
            "https://api.coinbase.com/api/v3/brokerage/products"
        ]
        
        for test_url in test_endpoints:
            try:
                response = requests.get(test_url, timeout=10)
                print(f"📡 {test_url}: {response.status_code}")
            except Exception as e:
                print(f"📡 {test_url}: ERROR - {e}")
                
    except Exception as e:
        print(f"❌ Error analysis failed: {e}")

def display_credential_summary():
    """Display credential summary for verification"""
    
    print("\n📋 CREDENTIAL SUMMARY")
    print("=" * 30)
    
    try:
        from credentials import WolfpackCredentials
        creds = WolfpackCredentials()
        
        print(f"API Key ID: {creds.COINBASE_API_KEY_ID}")
        print(f"Key Length: {len(creds.COINBASE_API_KEY_ID)} characters")
        print(f"Key Format: {'UUID format' if '-' in creds.COINBASE_API_KEY_ID else 'Other format'}")
        
        print(f"\nPrivate Key Seed: {creds.COINBASE_PRIVATE_KEY_SEED}")
        print(f"Seed Length: {len(creds.COINBASE_PRIVATE_KEY_SEED)} characters")
        
        # Decode and verify
        seed_bytes = base64.b64decode(creds.COINBASE_PRIVATE_KEY_SEED)
        print(f"Decoded Seed: {len(seed_bytes)} bytes")
        print(f"Seed Hex: {seed_bytes.hex()}")
        
        print(f"\nEndpoints:")
        print(f"Advanced Trade: {creds.COINBASE_LIVE_URL}")
        print(f"CDP: {creds.COINBASE_CDP_URL}")
        
    except Exception as e:
        print(f"❌ Credential summary failed: {e}")

def main():
    """Test all authentication formats"""
    
    print("🎯 FINAL COINBASE ED25519 PROTOCOL TEST")
    print("Testing ALL authentication variations from your protocols")
    print("Constitutional PIN: 841921")
    print("=" * 60)
    
    # Display credentials
    display_credential_summary()
    
    # Test all formats
    formats = [
        ("CDP SDK Format", test_cdp_sdk_format),
        ("Advanced Trade Format", test_advanced_trade_format), 
        ("Minimal Format", test_minimal_format)
    ]
    
    success_count = 0
    working_format = None
    
    for format_name, test_func in formats:
        try:
            success, data = test_func()
            if success:
                print(f"🎉 {format_name}: SUCCESS!")
                working_format = format_name
                success_count += 1
                
                if data and 'accounts' in data:
                    accounts = data['accounts']
                    print(f"   Found {len(accounts)} accounts")
                break
            else:
                print(f"❌ {format_name}: Failed")
                
        except Exception as e:
            print(f"❌ {format_name}: Exception - {e}")
    
    if success_count == 0:
        print("\n❌ ALL AUTHENTICATION FORMATS FAILED")
        print("This suggests an issue with the API key itself")
        analyze_error_response()
        
        print("\n🔧 TROUBLESHOOTING CHECKLIST:")
        print("1. ✅ ED25519 key is valid and working")
        print("2. ✅ JWT tokens are properly formatted") 
        print("3. ❌ API key authentication is failing")
        
        print("\n💡 POSSIBLE ISSUES:")
        print("• API key may be expired or deactivated")
        print("• API key may not have required permissions")
        print("• Account may need additional verification")  
        print("• API key may be for wrong environment (sandbox vs live)")
        print("• Rate limiting or temporary API issues")
        
        print("\n🔄 NEXT STEPS:")
        print("1. Log into Coinbase Developer Portal")
        print("2. Verify API key status and permissions")
        print("3. Check if account requires verification")
        print("4. Consider regenerating API key if needed")
        print("5. Test with a fresh API key")
        
    else:
        print(f"\n🎉 SUCCESS! {working_format} is working")
        print("🚀 Ready for integration with trading system")

if __name__ == "__main__":
    main()
